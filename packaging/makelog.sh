#!/bin/bash

mainlog="CHANGELOG"
debianlog="debian/changelog"
pypilog="../library/CHANGELOG.txt"

# generate debian changelog

cat $mainlog > $debianlog

# generate pypi changelog

sed -e "/--/d" -e "s/  \*/\*/" \
    -e "s/.*\([0-9].[0-9].[0-9]\).*/\1/" \
    -e '/[0-9].[0-9].[0-9]/ a\
    -----' $mainlog | cat -s > $pypilog

exit 0
