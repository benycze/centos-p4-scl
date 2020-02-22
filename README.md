# SCL P4 Repository with the SCL environment

[![Build Status](https://travis-ci.com/benycze/centos-p4-scl.svg?branch=master)](https://travis-ci.com/benycze/centos-p4-scl)
  
The repository containes files requird for building and translation of projects related to [P4](https://github.com/p4lang) language.

Currently, the environment allows to build and use:
* [P4C](https://github.com/p4lang/p4c)  
* [Behavioral Model](https://github.com/p4lang/behavioral-model)

## How to build the package

*This SCL environment is prepared for the Centos 7 Release*

The package has a dependency on additional devtoolset packages. Therefore, you need to be able to install such packages to build it:
* scl-utils-build 
* rpm-build
* devtoolset-6
* wget 
* binutils 
* cmake3
* git 
* autoconf 
* automake 
* libtool
* python-pip
* libatomic_ops-devel
* bison
* flex
* openssl-devel
* boost169-devel
* boost-devel-static

In Centos 7, these packages are available in `centos-release-scl-rh` or `centos-release-scl`. So, you need to additionaly install these
packages:

```
yum install centos-release-scl-rh epel-release
```

Install following packages which are required for the build:

```
yum install scl-utils scl-utils-build rpm-build devtoolset-6 wget binutils cmake3 git autoconf automake libtool python-pip libatomic_ops-devel bison flex openssl-devel boost169-devel boost-devel-static
```

The package can be builded like following:

```
rpmbuild -bb p4scl.spec --define 'scl p4lang-p4-1'
```

Install generated RPMS (find the rpmbuild folder):

```
yum localinstall ~/rpmbuild/RPMS/*/*.rpm
```

After the instalation you can run the environment:

```
scl enable p4lang-p4-1 bash
```

## How to test the build inside the environment

If you want to test the build, you can run the `test/test-build.sh` script which tries to translate and install packages using the `make install`. 

## Sources

SCL build documentation: https://www.softwarecollections.org/en/docs/guide/

## Authors:

* Pavel Benacek 

Contributions from other authors are welcomed!!

P.S. Sorry if something is not perfect but I am using the [Debian](https://www.debian.org) and this is one of my first attemps for RPMs :-). If you want to improve something, feel free to send me a merge request ;-).

