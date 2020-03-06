#!/usr/bin/env bash

# Copyright 2020 by the project contributors
# SPDX-License-Identifier: GPL-3.0-only
#
# Author(s): Pavel Benacek <pavel.benacek@gmail.com>

scl enable p4lang-p4-1 - << -EOF

    set -e
   
    if [ $1 = "p4c" ]; then 
        echo "####################################################"
        echo Testing compilation of P4C
        echo "####################################################"
        
        git clone --recursive https://github.com/p4lang/p4c p4c.git
        cd p4c.git
        mkdir build extensions
        cd build 
        cmake3 -DBoost_DEBUG=on ..
        make -j2
        make install
        make uninstall 
    
        echo "P4C is possible to build ..."
        exit 0
    fi
   

    if [ $1 = "bmv2" ]; then 
        echo "####################################################"
        echo Testing compilation of behavioral model
        echo "####################################################"
        
        git clone --recursive https://github.com/p4lang/behavioral-model behavioral-model.git
        cd behavioral-model.git
        bash autogen.sh
        ./configure
        make -j2
        make install
        make uninstall

        echo "bmv2 is possible to build ..."
        exit 1
    fi
    

exit 0

-EOF
