#!/bin/bash

# script control variables

libname="" # leave this blank for auto-detection
vlibwarn="yes"

debdir="$(pwd)"
rootdir="$(dirname $debdir)"
libdir="$rootdir/library"

mainlog="CHANGELOG"
debianlog="debian/changelog"
pypilog="$libdir/CHANGELOG.txt"

# function define

success() {
    echo "$(tput setaf 2)$1$(tput sgr0)"
}

inform() {
    echo "$(tput setaf 6)$1$(tput sgr0)"
}

warning() {
    echo "$(tput setaf 1)$1$(tput sgr0)"
}

newline() {
    echo ""
}

# generate debian changelog

cat $mainlog > $debianlog
inform "seeded debian changelog"

# generate pypi changelog

sed -e "/--/d" -e "s/  \*/\*/" \
    -e "s/.*\([0-9].[0-9].[0-9]\).*/\1/" \
    -e '/[0-9].[0-9].[0-9]/ a\
-----' $mainlog | cat -s > $pypilog

version=$(head -n 1 $pypilog)
inform "pypi changelog generated"

# touch up version in setup.py file

if [ -n $(grep version "$libdir/setup.py" &> /dev/null) ]; then
    inform "touched up version in setup.py"
    sed -i "s/[0-9].[0-9].[0-9]/$version/" "$libdir/setup.py"
else
    warning "couldn't touch up version in setup, no match found"
fi

# touch up version in lib

if [ -z "$libname" ]; then
    cd "$libdir"
    libname=$(grep "name" setup.py | tr -d "[:space:]" | cut -c 7- | rev | cut -c 3- | rev)
    libname=$(echo "$libname" | tr "[A-Z]" "[a-z]") && cd "$debdir"
fi

if grep -e "__version__" "$libdir/$libname.py" &> /dev/null; then
    sed -i "s/__version__ = '[0-9].[0-9].[0-9]/__version__ = '$version/" "$libdir/$libname.py"
    inform "touched up version in $(basename $libdir/$libname.py)"
elif grep -e "__version__" "$libdir/$libname/__init__.py" &> /dev/null; then
    sed -i "s/__version__ = '[0-9].[0-9].[0-9]/__version__ = '$version/" "$libdir/$libname/__init__.py"
    inform "touched up version in $(basename $libdir/$libname/__init__.py)"
elif [ "$vlibwarn" == "yes" ]; then
    warning "couldn't touch up __version__ in lib, no match found"
fi

exit 0
