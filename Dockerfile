# Copyright 2020 by the project contributors
# SPDX-License-Identifier: GPL-3.0-only
#
# Author(s): Pavel Benacek <pavel.benacek@gmail.com>

FROM centos:latest

# Dependents to install
ENV DEPS autoconf automake binutils bison flex gcc gcc-c++ gdb glibc-devel libtool make pkgconf pkgconf-m4 pkgconf-pkg-config redhat-rpm-config rpm-build rpm-sign strace asciidoc byacc ctags diffstat git intltool jna ltrace patchutils perl-Fedora-VSP perl-generators pesign source-highlight systemtap valgrind valgrind-devel cmake expect rpmdevtools rpmlint scl-utils scl-utils-build wget binutils cmake python2-pip python3-pip openssl-devel boost169-devel boost169-static libffi-devel boost-devel python2-devel python36-devel libpcap-devel gc-devel

# Switch to centos stream release
RUN dnf clean all && dnf install -y centos-release-stream && dnf swap -y centos-{linux,stream}-repos && dnf distro-sync -y
# Install all dependencies
RUN dnf upgrade -y &&  dnf update -y && dnf install -y epel-release dnf-plugins-core && dnf config-manager --set-enabled powertools && dnf install -y $DEPS

# Prepare the directory
RUN mkdir /centos-p4-scl.git
COPY . /centos-p4-scl.git
WORKDIR /centos-p4-scl.git
