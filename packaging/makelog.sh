#!/bin/bash

debianlog="debian/changelog"
releaselog="../library/CHANGELOG.txt"

sed -e "/--/d" -e "s/  \*/\*/" \
    -e "s/.*\([0-9].[0-9].[0-9]\).*/\1/" \
    -e '/[0-9].[0-9].[0-9]/ a\
    -----' $debianlog | cat -s > $releaselog

exit 0
