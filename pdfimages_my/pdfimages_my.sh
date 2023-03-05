#! /bin/sh
#
# pdfimages_my.sh
# Copyright (C) 2017 abunbux <abunbux@pasha>
#
# Distributed under terms of the MIT license.
#


for file in *.pdf
do
	PDF=`basename "$file"`
	NAME="2. + $PDF"
	pdfimages -f 1 -l 1 -j "$file" "$NAME"
done
exit 0

