#!/bin/bash

# script control variables

reponame="" # leave this blank for auto-detection
libname="" # leave this blank for auto-detection
packagename="" # leave this blank for auto-selection

debianlog="debian/changelog"
debcontrol="debian/control"
debcopyright="debian/copyright"
debrules="debian/rules"
debreadme="debian/README"

debdir="$(pwd)"
rootdir="$(dirname $debdir)"
libdir="$rootdir/library"

FLAG=false

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

# assessing repo and library variables

if [ -z "$reponame" ] || [ -z "$libname" ]; then
    inform "detecting reponame and libname..."
else
    inform "using reponame and libname overrides"
fi

if [ -z "$reponame" ]; then
    if [[ $rootdir == *"python"* ]]; then
        repodir="$(dirname $rootdir)"
        reponame="$(basename $repodir)"
    else
        repodir="$rootdir"
        reponame="$(basename $repodir)"
    fi
    reponame=$(echo "$reponame" | tr "[A-Z]" "[a-z]")
fi

if [ -z "$libname" ]; then
    cd "$libdir"
    libname=$(grep "name" setup.py | tr -d "[:space:]" | cut -c 7- | rev | cut -c 3- | rev)
    libname=$(echo "$libname" | tr "[A-Z]" "[a-z]") && cd "$debdir"
fi

if [ -z "$packagename" ]; then
    packagename="$libname"
fi

echo "reponame is $reponame and libname is $libname"
echo "output packages will be python-$packagename and python3-$packagename"

# checking generating changelog file

./makelog.sh
version=$(head -n 1 "$libdir/CHANGELOG.txt")
echo "building $libname version $version"

# checking debian/changelog file

inform "checking debian/changelog file..."

if ! head -n 1 $debianlog | grep "$libname" &> /dev/null; then
    warning "library not mentioned in header!" && FLAG=true
elif head -n 1 $debianlog | grep "UNRELEASED"; then
    warning "this changelog is not going to generate a release!"
    warning "change distribution to 'stable'" && FLAG=true
fi

# checking debian/copyright file

inform "checking debian/copyright file..."

if ! grep "^Source" $debcopyright | grep "$reponame" &> /dev/null; then
    warning "$(grep "^Source" $debcopyright)" && FLAG=true
fi

if ! grep "^Upstream-Name" $debcopyright | grep "$libname" &> /dev/null; then
    warning "$(grep "^Upstream-Name" $debcopyright)" && FLAG=true
fi

# checking debian/control file

inform "checking debian/control file..."

if ! grep "^Source" $debcontrol | grep "$libname" &> /dev/null; then
    warning "$(grep "^Source" $debcontrol)" && FLAG=true
fi

if ! grep "^Homepage" $debcontrol | grep "$reponame" &> /dev/null; then
    warning "$(grep "^Homepage" $debcontrol)" && FLAG=true
fi

if ! grep "^Package: python-$packagename" $debcontrol &> /dev/null; then
    warning "$(grep "^Package: python-" $debcontrol)" && FLAG=true
fi

if ! grep "^Package: python3-$packagename" $debcontrol &> /dev/null; then
    warning "$(grep "^Package: python3-" $debcontrol)" && FLAG=true
fi

if ! grep "^Priority: extra" $debcontrol &> /dev/null; then
    warning "$(grep "^Priority" $debcontrol)" && FLAG=true
fi


# checking debian/rules file

inform "checking debian/rules file..."

if ! grep "debian/python-$packagename" $debrules &> /dev/null; then
    warning "$(grep "debian/python-" $debrules)" && FLAG=true
fi

if ! grep "debian/python3-$packagename" $debrules &> /dev/null; then
    warning "$(grep "debian/python3-" $debrules)" && FLAG=true
fi

# checking debian/README file

inform "checking debian/readme file..."

if ! grep -e "$libname" -e "$reponame" $debreadme &> /dev/null; then
    warning "README does not seem to mention product, repo or lib!" && FLAG=true
fi

# summary of checks pre build

if $FLAG; then
    warning "Check all of the above and correct!" && exit 1
else
    inform "we're good to go... bulding!"
fi

# building deb and final checks

./makedeb.sh

inform "running lintian..."
lintian -v $(find -name "python*$version*.deb")
lintian -v $(find -name "python3*$version*.deb")

inform "checking signatures..."
gpg --verify $(find -name "*$version*changes")
gpg --verify $(find -name "*$version*dsc")

exit 0
