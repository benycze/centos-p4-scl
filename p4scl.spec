# Copyright 2020 by the project contributors
# SPDX-License-Identifier: GPL-3.0-only
#
# Author(s): Pavel Benacek <pavel.benacek@gmail.com>

# Disable debug info package
%define debug_package %{nil}

%global scl_name_prefix p4lang-
%global scl_name_base p4

%global scl %{scl_name_prefix}%{scl_name_base}

%global scl_ipath %{buildroot}%{_scl_root}
%global scl_bpath %{_builddir}/pkgbuild

#%global build_cpus 3
%global build_cpus 8

%global nfsmountable 1
%scl_package %scl

Summary: Package that installs %scl environment for the P4 related projects
Name: %scl_name
Version: 1
Release: 1%{?dist}
License: GPLv3+
# Tools for development
Requires: autoconf automake binutils bison flex gcc gcc-c++ gdb glibc-devel libtool make cmake pkgconf pkgconf-m4 pkgconf-pkg-config
Requires: redhat-rpm-config rpm-build rpm-sign strace asciidoc byacc ctags diffstat git intltool jna ltrace patchutils
Requires:perl-Fedora-VSP perl-generators pesign source-highlight systemtap valgrind valgrind-devel expect rpmdevtools rpmlint
Requires: scl-utils-build wget git python2-pip python3-pip boost169-devel libatomic_ops openssl-devel boost169-static boost
Requires: scl-utils python2-setuptools python3-setuptools Judy-devel gmp-devel libpcap
Requires: libevent-devel openssl-devel readline-devel libpcap-devel gc-devel

Requires: python3-scapy  boost169-devel boost169-static boost python36-devel python2-devel

%description
This is the main package for %scl Software Collection which can be used on building of p4lang projects on Centos 8 without any container.

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


# Enable the environment and install all required libraries
bash << -EOF
    set -e
    # Remove the build directory and create it again
    rm -rf %{scl_bpath}
    mkdir -p %{scl_bpath}
    
    export CXXFLAGS="-g0 -O2" 
    export CFLAGS="-g0 -O2" 
    export PY_PREFIX=%{_scl_root}/usr

    echo "#####################################################"
    echo "Build the thrift library"
    echo "#####################################################"
    cd %{scl_bpath}
    pushd .
    wget -O thrift-0.11.0.tar.gz https://github.com/apache/thrift/archive/0.11.0.tar.gz
    tar -xzvf thrift-0.11.0.tar.gz
    cd thrift-0.11.0 
    # Compile the program
    ./bootstrap.sh
    ./configure --prefix=%{_scl_root}/usr --with-cpp --disable-tests 
    make -j%{build_cpus}
    popd

    # Some libs need to be installed in root directory because of the cmake and others.
    # We will install them to the /usr/local path

    echo "#####################################################"
    echo "Build the nanomsg library"
    echo "#####################################################"
    pushd .
    wget -O nanomsg-1.0.0.tar.gz https://github.com/nanomsg/nanomsg/archive/1.0.0.tar.gz
    tar -xvzf nanomsg-1.0.0.tar.gz 
    cd nanomsg-1.0.0
    mkdir build 
    cd build
    cmake3 -DCMAKE_INSTALL_PREFIX=/usr/local -DCMAKE_BUILD_TYPE=Release ..
    make -j%{build_cpus}
    popd

    echo "#####################################################"
    echo "Build the protobuf library"
    echo "#####################################################"
    pushd .
    git clone https://github.com/google/protobuf.git protobuf;
    cd protobuf;
    git checkout v3.6.1
    bash ./autogen.sh
    ./configure --prefix=/usr/local
    make -j%{build_cpus} 
    popd
    
-EOF


%install
%scl_install

# #########################################################
# Install libs & tools

# Some libs requires a g++ during install :/
bash << -EOF
    set -e
    
    export CXXFLAGS="-g0 -O2" 
    export CFLAGS="-g0 -O2" 
    export PY_PREFIX=%{_scl_root}/usr

    echo "#####################################################"
    echo "Library & tool install"
    echo "#####################################################"

    cd %{scl_bpath}
    
    # Install compiled stuff 
    (cd thrift-0.11.0; %make_install;)
    (cd nanomsg-1.0.0/build; %make_install)
    (cd protobuf; %make_install)

-EOF

# #########################################################
# Preare the enable file

cat >> %{buildroot}%{_scl_scripts}/enable << -EOF
# Enable the remaining parts for the P4 scl
export PATH="%{_bindir}:%{_sbindir}\${PATH:+:\${PATH}}"
export LIBRARY_PATH="/usr/lib64/boost169:/usr/local/lib:/usr/local/lib64:%{_libdir}:%{_scl_root}/usr/lib\${LIBRARY_PATH:+:\${LIBRARY_PATH}}"
export LD_LIBRARY_PATH="/usr/lib64/boost169:/usr/local/lib:/usr/local/lib64:%{_libdir}:%{_scl_root}/usr/lib\${LD_LIBRARY_PATH:+:\${LD_LIBRARY_PATH}}"
export MANPATH="%{_mandir}:\${MANPATH:-}"
export PKG_CONFIG_PATH="/usr/local/lib/pkgconfig:%{_libdir}/pkgconfig:%{_scl_root}/usr/lib/pkgconfig\${PKG_CONFIG_PATH:+:\${PKG_CONFIG_PATH}}"
export PYTHONPATH="/usr/local/lib64/python2.7/site-packages:%{_scl_root}/usr/lib/python2.7/site-packages\${PYTHONPATH:+:\${PYTHONPATH}}"
export C_INCLUDE_PATH="/usr/local/include:%{_scl_root}/usr/include\${C_INCLUDE_PATH:+:\${C_INCLUDE_PATH}}"
export CPLUS_INCLUDE_PATH="/usr/local/include:%{_scl_root}/usr/include\${CPLUS_INCLUDE_PATH:+:\${CPLUS_INCLUDE_PATH}}"

# Setup boost environment to newest version
#export BOOST_INCLUDEDIR=/usr/include/boost169
#export BOOST_LIBRARYDIR=/usr/lib64/boost169

-EOF


%files

%files runtime -f filelist
%scl_files
%{_scl_root}/usr/lib/*
/usr/local/*

%files build
%{_root_sysconfdir}/rpm/macros.%{scl}-config

%changelog
* Tue Apr 28 2020 Pavel Benacek %lt;pavel.benacek@gmail.com&gt; 1-2
- Transformation of the spec file to Centos 8

* Thu Feb 20 2020 Pavel Benacek %lt;pavel.benacek@gmail.com&gt; 1-1
- Update of enable script

* Wed Feb 19 2020 Pavel Benacek &lt;pavel.benacek@gmail.com&gt; 1-0
- Initial package
