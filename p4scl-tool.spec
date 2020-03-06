# Copyright 2020 by the project contributors
# SPDX-License-Identifier: GPL-3.0-only
#
# Author(s): Pavel Benacek <pavel.benacek@gmail.com>

# Disable debug info package
%define debug_package %{nil}

# TODO: Better fix of the Python build error
%define _python_bytecompile_errors_terminate_build 0

%global scl_name_prefix p4lang-
%global scl_name_base p4devel-
%global scl_name_version 1

%global scl %{scl_name_prefix}%{scl_name_base}%{scl_name_version}

%global scl_ipath %{buildroot}%{_scl_root}
%global scl_bpath %{_builddir}/pkgbuild

%global build_cpus 3

%global nfsmountable 1
%scl_package %scl

Summary: Package that installs %scl environment for the P4 related projects
Name: %scl_name
Version: 1
Release: 1%{?dist}
License: GPLv3+
BuildRequires:p4lang-p4-1 libffi-devel
Requires: %scl_require p4lang-p4-1
Requires: libffi-devel

%description
This is the main package for %scl Software Collection with additonal tools to run verifications and models.

%package runtime
Summary: Package that handles %scl Software Collection.
Requires: scl-utils

%description runtime
Package shipping essential scripts to work with %scl Software Collection.

%package build
Summary: Package shipping basic build configuration
Requires: scl-utils-build

%description build
Package shipping essential configuration macros to build %scl Software Collection.

%prep
%setup -c -T

%build


# Enable the environment and install all required tools
scl enable p4lang-p4-1 - << -EOF
    set -e
    # Remove the build directory and create it again
    rm -rf %{scl_bpath}
    mkdir -p %{scl_bpath}
    
    export CXXFLAGS="-g0 -O2" 
    export CFLAGS="-g0 -O2" 
    export PY_PREFIX=%{_scl_root}/usr
    
    cd %{scl_bpath}

    echo "#####################################################"
    echo "Build the nnpy"
    echo "#####################################################"
    git clone --recursive https://github.com/nanomsg/nnpy nnpy.git

    echo "#####################################################"
    echo "Build the BMv2 model"
    echo "#####################################################"
    pushd .
    git clone --recursive https://github.com/p4lang/behavioral-model bmv2.git
    cd bmv2.git
    # Compile the program
    ./autogen.sh
    ./configure --prefix=%{_scl_root}/usr
    make -j%{build_cpus}
    popd

    echo "#####################################################"
    echo "Build the P4C tools"
    echo "#####################################################"
    pushd .
    git clone --recursive https://github.com/p4lang/p4c p4c.git
    cd p4c.git
    mkdir build 
    cd build
    cmake3 -DCMAKE_INSTALL_PREFIX=%{_scl_root}/usr -DCMAKE_BUILD_TYPE=Release ..
    make -j%{build_cpus}
    popd 

    echo "#####################################################"
    echo "Build p4pktgen"
    echo "#####################################################"
    git clone --recursive https://github.com/p4pktgen/p4pktgen p4pktgen.git   
 
-EOF


%install
%scl_install

# #########################################################
# Install libs & tools

scl enable p4lang-p4-1 - << -EOF
    set -e
    
    export CXXFLAGS="-g0 -O2" 
    export CFLAGS="-g0 -O2" 
    export PY_PREFIX=%{_scl_root}/usr

    echo "#####################################################"
    echo "Library & tool install"
    echo "#####################################################"

    cd %{scl_bpath}

    # Install compiled stuff 
    (cd bmv2.git; %make_install;)
    (cd p4c.git/build; %make_install;)
    
    # Install python stuff
    (cd nnpy.git; pip2 install --compile --root=%{scl_ipath} .)
    # Requirements are installed manually because we are not able to install python unit test tool
    (cd p4pktgen.git; 
     pip2 install --compile --root=%{scl_ipath}  enum34==1.1.6 functools32==3.2.3.post2 graphviz==0.8 scapy==2.4.3 subprocess32==3.5.3 thrift==0.11.0 z3-solver==4.8.0.0.post1; 
     pip2 install --compile --root=%{scl_ipath} .)

-EOF

# #########################################################
# Preare the enable file

cat >> %{buildroot}%{_scl_scripts}/enable << -EOF
# Enable the environment for the build of P4 tools
source scl_source enable p4lang-p4-1
# Enable the remaining parts for the P4 scl
export PATH="%{_scl_root}/usr/bin:%{_scl_root}/usr/local/bin:%{_bindir}:%{_sbindir}\${PATH:+:\${PATH}}"
export LIBRARY_PATH="%{_libdir}:%{_scl_root}/usr/lib:%{_scl_root}/usr/lib64\${LIBRARY_PATH:+:\${LIBRARY_PATH}}"
export LD_LIBRARY_PATH="%{_libdir}:%{_scl_root}/usr/lib:%{_scl_root}/usr/lib64/\${LD_LIBRARY_PATH:+:\${LD_LIBRARY_PATH}}"
export MANPATH="%{_mandir}:\${MANPATH:-}"
export PKG_CONFIG_PATH="%{_libdir}/pkgconfig:%{_scl_root}/usr/lib/pkgconfig\${PKG_CONFIG_PATH:+:\${PKG_CONFIG_PATH}}"
export PYTHONPATH="%{_scl_root}/usr/lib64/python2.7/site-packages:%{_scl_root}/usr/lib/python2.7/site-packages\${PYTHONPATH:+:\${PYTHONPATH}}"
export C_INCLUDE_PATH="%{_scl_root}/usr/include\${C_INCLUDE_PATH:+:\${C_INCLUDE_PATH}}"
export CPLUS_INCLUDE_PATH="%{_scl_root}/usr/include\${CPLUS_INCLUDE_PATH:+:\${CPLUS_INCLUDE_PATH}}"

-EOF


%files

%files runtime -f filelist
%scl_files
%{_scl_root}/usr/*

%files build
%{_root_sysconfdir}/rpm/macros.%{scl}-config

%changelog
* Wed Feb 19 2020 Pavel Benacek &lt;pavel.benacek@gmail.com&gt; 1-0
- Initial package for the tool building
