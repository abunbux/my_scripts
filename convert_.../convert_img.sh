#!/bin/sh


for file in *.CHK
do
    IMG=`basename "$file" ".CHK"`".jpg"
    convert $file $IMG
done
