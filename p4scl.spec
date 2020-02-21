# Copyright 2020 by the project contributors
# SPDX-License-Identifier: GPL-3.0-only
#
# Author(s): Pavel Benacek <pavel.benacek@gmail.com>

# Disable debug info package
%define debug_package %{nil}

%global scl_name_prefix p4lang-
%global scl_name_base p4-
%global scl_name_version 1

%global scl %{scl_name_prefix}%{scl_name_base}%{scl_name_version}

%global scl_ipath %{buildroot}%{_scl_root}
%global scl_bpath %{_builddir}/pkgbuild

%global build_cpus 2

%global nfsmountable 1
%scl_package %scl

Summary: Package that installs %scl environment for the P4 related projects
Name: %scl_name
Version: 1
Release: 1%{?dist}
License: GPLv3+
BuildRequires: scl-utils-build devtoolset-6 wget binutils cmake3 git autoconf automake libtool python-pip boost169-devel libatomic_ops-devel bison flex openssl-devel boost-devel-static
Requires: %scl_require devtoolset-6 
Requires: scl-utils cmake3 doxygen python-pip python-setuptools automake Judy-devel gmp-devel libpcap-devel
Requires: libevent-devel libtool flex pkgconfig openssl-devel python-devel readline-devel bison 
Requires: autoconf libtool python-pip scapy libatomic_ops-devel openssl-devel boost169-devel boost-devel-static

%description
This is the main package for %scl Software Collection which can be used on building of p4lang projects on Centos 7 without any container.

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
scl enable devtoolset-6 - << -EOF
    set -e
    # Remove the build directory and create it again
    rm -rf %{scl_bpath}
    mkdir -p %{scl_bpath}
    
    export CXXFLAGS="-g0 -O2" 
    export CFLAGS="-g0 -O2" 
    export PY_PREFIX=%{_scl_root}/usr

    echo #####################################################
    echo "Build the thrift library"
    echo #####################################################
    cd %{scl_bpath}
    pushd .
    wget -O thrift-0.11.0.tar.gz https://github.com/apache/thrift/archive/0.11.0.tar.gz
    tar -xzvf thrift-0.11.0.tar.gz
    cd thrift* 
    # Compile the program
    ./bootstrap.sh
    ./configure --prefix=%{_scl_root}/usr --with-cpp
    make -j%{build_cpus}
    popd

    # Some libs need to be installed in root directory because of the cmake and others.
    # We will install them to the /usr/local path

    echo #####################################################
    echo "Build the nanomsg library"
    echo #####################################################
    pushd .
    wget -O nanomsg-1.0.0.tar.gz https://github.com/nanomsg/nanomsg/archive/1.0.0.tar.gz
    tar -xvzf nanomsg-1.0.0.tar.gz 
    cd nanomsg-1.0.0
    mkdir build 
    cd build
    cmake3 -DCMAKE_INSTALL_PREFIX=/usr/local -DCMAKE_BUILD_TYPE=Release ..
    make -j%{build_cpus}
    popd

    echo #####################################################
    echo "Build the protobuf library"
    echo #####################################################
    pushd .
    git clone https://github.com/google/protobuf.git protobuf;
    cd protobuf;
    git checkout v3.6.1
    bash ./autogen.sh
    ./configure --prefix=/usr/local
    make -j%{build_cpus} 
    popd
    
    echo #####################################################
    echo "Install new gc library"
    echo #####################################################
    pushd .
    wget https://github.com/ivmai/bdwgc/releases/download/v7.4.18/gc-7.4.18.tar.gz
    tar -xvzf gc-7.4.18.tar.gz
    cd gc-7.4.18
    bash autogen.sh
    ./configure --prefix=%{_scl_root}/usr --enable-cplusplus --enable-parallel-mark --enable-sigrt-signals
    make -j%{build_cpus}
    popd

-EOF


%install
%scl_install

# #########################################################
# Install libs & tools

# Some libs requires a g++ during install :/
scl enable devtoolset-6 - << -EOF
    set -e
    
    export CXXFLAGS="-g0 -O2" 
    export CFLAGS="-g0 -O2" 
    export PY_PREFIX=%{_scl_root}/usr

    echo #####################################################
    echo "Library & tool install"
    echo #####################################################

    cd %{scl_bpath}
    
    # Install compiled stuff 
    (cd thrift-0.11.0; %make_install;)
    (cd nanomsg-1.0.0/build; %make_install)
    (cd protobuf; %make_install)
    (cd gc-7.4.18; %make_install)

-EOF

# #########################################################
# Preare the enable file

cat >> %{buildroot}%{_scl_scripts}/enable << -EOF
# Enable the environment for the build 
source scl_source enable devtoolset-6
# Enable the remaining parts for the P4 scl
export PATH="%{_bindir}:%{_sbindir}\${PATH:+:\${PATH}}"
export LIBRARY_PATH="/usr/local/lib:%{_libdir}:%{_scl_root}/usr/lib\${LIBRARY_PATH:+:\${LIBRARY_PATH}}"
export LD_LIBRARY_PATH="/usr/local/lib:%{_libdir}:%{_scl_root}/usr/lib\${LD_LIBRARY_PATH:+:\${LD_LIBRARY_PATH}}"
export MANPATH="%{_mandir}:\${MANPATH:-}"
export PKG_CONFIG_PATH="/usr/local/lib/pkgconfig:%{_libdir}/pkgconfig:%{_scl_root}/usr/lib/pkgconfig\${PKG_CONFIG_PATH:+:\${PKG_CONFIG_PATH}}"
export PYTHONPATH="/usr/local/lib64/python2.7/site-packages:%{_scl_root}/usr/lib64/python2.7/site-packages\${PYTHONPATH:+:\${PYTHONPATH}}"
export C_INCLUDE_PATH="/usr/local/include:%{_scl_root}/usr/include\${C_INCLUDE_PATH:+:\${C_INCLUDE_PATH}}"
export CPLUS_INCLUDE_PATH="/usr/local/include:%{_scl_root}/usr/include\${CPLUS_INCLUDE_PATH:+:\${CPLUS_INCLUDE_PATH}}"

# Setup boost environment to newest version
export BOOST_INCLUDEDIR=/usr/include/boost169
export BOOST_LIBRARYDIR=/usr/lib64/:/usr/lib64/boost169

echo "*************************************************************************"
echo "WARNING: Use cmake3 instead of cmake"
echo "*************************************************************************"

-EOF


%files

%files runtime -f filelist
%scl_files
%{_scl_root}/usr/lib/*
/usr/local/*

%files build
%{_root_sysconfdir}/rpm/macros.%{scl}-config

%changelog
* Thu Feb 20 2020 Pavel Benacek %lt;pavel.benacek@gmail.com&gt; 1-1
- Update of enable script

* Wed Feb 19 2020 Pavel Benacek &lt;pavel.benacek@gmail.com&gt; 1-0
- Initial package
