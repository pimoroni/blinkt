#!/bin/bash

mainlog="CHANGELOG"
debianlog="debian/changelog"
pypilog="../library/CHANGELOG.txt"
setupfile="../library/setup.py"

# generate debian changelog

cat $mainlog > $debianlog

# generate pypi changelog

sed -e "/--/d" -e "s/  \*/\*/" \
    -e "s/.*\([0-9].[0-9].[0-9]\).*/\1/" \
    -e '/[0-9].[0-9].[0-9]/ a\
-----' $mainlog | cat -s > $pypilog

version=$(head -n 1 $pypilog)
sed -i "s/[0-9].[0-9].[0-9]/$version/" $setupfile

exit 0
