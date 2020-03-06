#!/usr/bin env bash

echo "#####################################################"
echo "Removing everything related to the P4"
echo "#####################################################"
PACKAGES=`yum list installed | grep p4lang- | awk '{print $1}'`
if [ -n "$PACKAGES" ]; then
    yum remove -y $PACKAGES
fi

echo "System is clear ..."

echo "#####################################################"
echo "Compiling & installing the P4 ENV package"
echo "#####################################################"

rpmbuild -bb p4scl.spec --define scl p4lang-p4-1

echo "Installing P4 ENV ..."
yum localinstall -y ~/rpmbuild/RPMS/x86_64/*

echo "#####################################################"
echo "Compiling & intalling the P4 TOOLS package"
echo "#####################################################"

rpmbuild -bb p4scl-tool.spec --define scl p4lang-p4devel-1

echo "Installing P4 TOOLS ..."
yum localinstall -y ~/rpmbuild/RPMS/x86_64/*

echo "We are done ...."
