# SCL P4 Repository with the SCL environment 

[![Build Status](https://benycze.semaphoreci.com/badges/centos-p4-scl/branches/master.svg?style=shields)](https://benycze.semaphoreci.com/projects/centos-p4-scl)

The repository containes files requird for building and translation of projects related to [P4](https://github.com/p4lang) language.

Currently, the environment allows to build and use:
* [P4C](https://github.com/p4lang/p4c)  
* [Behavioral Model](https://github.com/p4lang/behavioral-model)
* [p4pktgen](https://github.com/p4pktgen/p4pktgen)

## How to build packages

*This SCL environment is prepared for the Centos Stream Release*

The following dependencies are required to build RPM packages (this is typical development tools on Centos):
* autoconf
* automake
* binutils
* bison
* flex
* gcc
* gcc-c++
* gdb
* glibc-devel
* libtool
* make
* pkgconf
* pkgconf-m4
* pkgconf-pkg-config
* redhat-rpm-config
* rpm-build
* rpm-sign
* strace
* asciidoc
* byacc
* ctags
* diffstat
* git 
* intltool
* jna 
* ltrace
* patchutils
* perl-Fedora-VSP
* perl-generators
* pesign
* source-highlight
* systemtap
* valgrind
* valgrind-devel
* cmake
* expect
* rpmdevtools
* rpmlint
* scl-utils
* scl-utils-build
* wget
* binutils
* cmake
* python2-pip
* python3-pip
* openssl-devel
* boost169-devel
* boosti169-static
* libffi-devel
* boost-devel

Currently available spec files:

* `p4scl.spec` - SPEC file with libs to build mentioned projects.
* `p4scl-tool.spec` - SPEC file with tools (p4c, behavioral model, p4pktgen). It requies packages RPM packages builded from the `p4scl.spec` file. The environment contains everything from p4scl.spec packages.


On Centos 8, install the EPEL and dnf plugins:

```
dnf install epel-release dnf-plugins-core
```

We also need to enable the PowerTools repository (to get some libs):

```
dnf config-manager --set-enabled powertools
```

Install following packages which are required for the build:

```
dnf install autoconf automake binutils bison flex gcc gcc-c++ gdb glibc-devel libtool make pkgconf pkgconf-m4 pkgconf-pkg-config redhat-rpm-config rpm-build rpm-sign strace asciidoc byacc ctags diffstat git intltool jna ltrace patchutils perl-Fedora-VSP perl-generators pesign source-highlight systemtap valgrind valgrind-devel cmake expect rpmdevtools rpmlint scl-utils scl-utils-build wget binutils cmake python2-pip python3-pip openssl-devel boost169-devel boost169-static libffi-devel boost-devel python36-devel python2-devel libpcap-devel gc-devel
```

The P4 Environment package can be builded like following:

```
rpmbuild -bb p4scl.spec --define 'scl p4lang-p4'
```

Install generated RPMS (find the rpmbuild folder):

```
dnf localinstall ~/rpmbuild/RPMS/*/*.rpm
```

After the instalation you can run the environment:

```
scl enable p4lang-p4 bash
```

Very similarly can be build the package with tools. You can also run the `compile-and-install.sh` script which removes all `p4lang` packages in the system. After that, it build RPM packages and install everything from scratch. You can also inspect that file to see how you can build all RPM packages.

## Sources

SCL build documentation: https://www.softwarecollections.org/en/docs/guide/

## Authors:

* Pavel Benáček

Contributions from other authors are welcomed!!

P.S. Sorry if something is not perfect but I am using the [Debian](https://www.debian.org) and this is one of my first attemps for RPMs :-). If you want to improve something, feel free to send me a merge request ;-).
