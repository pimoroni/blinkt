#!/bin/bash

gettools="no" # if set to yes downloads the tools required
setup="yes" # if set to yes populates library folder
buildeb="yes" # if set to yes builds the deb files
cleanup="yes" # if set to yes cleans up build files
pkgfiles=( "build" "changes" "deb" "dsc" "tar.xz" )

if [ $gettools == "yes" ]; then
    sudo apt-get update && sudo apt-get install build-essential debhelper devscripts dh-make dh-python dput gnupg
    sudo apt-get install python-all python-setuptools python3-all python3-setuptools
    sudo apt-get install python-mock python-sphinx python-sphinx-rtd-theme
    sudo pip install Sphinx --upgrade && sudo pip install sphinx_rtd_theme --upgrade
fi

if [ $setup == "yes" ]; then
    rm -R ../library/build ../library/debian &> /dev/null
    cp -R ./debian ../library/ && cp -R ../sphinx ../library/doc
fi

cd ../library

if [ $buildeb == "yes" ]; then
    debuild -aarmhf
    for file in ${pkgfiles[@]}; do
        rm ../packaging/*.$file &> /dev/null
        mv ../*.$file ../packaging
    done
    rm -R ../documentation/html &> /dev/null
    cp -R ./build/sphinx/html ../documentation
fi

if [ $cleanup == "yes" ]; then
    debuild clean
    rm -R ./build ./debian ./doc &> /dev/null
fi

exit 0
