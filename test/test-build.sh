#!/usr/bin/env bash

# Copyright 2020 by the project contributors
# SPDX-License-Identifier: GPL-3.0-only
#
# Author(s): Pavel Benacek <pavel.benacek@gmail.com>

scl enable p4lang-p4-1 - << -EOF

    set -e
    
    rm -rf *.git
    
    echo "####################################################"
    echo Testing compilation of P4C
    echo "####################################################"
    
    git clone --recursive https://github.com/p4lang/p4c p4c.git
    pushd .
    cd p4c.git
    mkdir build extensions
    cd build 
    cmake3 ..
    make -j1
    make install
    popd
    
    echo "####################################################"
    echo Testing compilation of behavioral model
    echo "####################################################"
    
    pushd .
    git clone --recursive https://github.com/p4lang/behavioral-model behavioral-model.git
    cd behavioral-model.git
    bash autogen.sh
    ./configure
    make -j1
    make install
    popd
    
    echo "It seems that we are able to compile everything ..."

    echo "####################################################"
    echo "It seems that we are able to compile everything ..."
    echo "####################################################"

    echo "Uninstalling all ..."
    (cd p4c.git/build; make uninstall;)
    (cd behavioral-model.git; make uninstall;)

-EOF
