# Copyright 2020 by the project contributors
# SPDX-License-Identifier: GPL-3.0-only
#
# Author(s): Pavel Benacek <pavel.benacek@gmail.com>

FROM centos:7

# Dependents to install
ENV DEPS scl-utils scl-utils-build rpm-build devtoolset-6 wget binutils cmake3 git autoconf automake libtool python-pip libatomic_ops-devel bison flex openssl-devel boost169-devel boost-devel-static libffi-devel

# Install all dependencies
RUN yum update -y && yum install -y centos-release-scl-rh epel-release
RUN yum install -y $DEPS

# Prepare the directory
RUN mkdir /centos-p4-scl.git
COPY . /centos-p4-scl.git
WORKDIR /centos-p4-scl.git

# Build & install all rpm packages
RUN ./compile-and-install.sh
