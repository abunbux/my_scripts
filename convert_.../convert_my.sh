#! /bin/sh
#
# convert_my.sh
# Copyright (C) 2017 abunbux <abunbux@pasha>
#
# Distributed under terms of the MIT license.
#

# В принципе, думаю, здесь всё понятно.
# Уменьшаем в директории картинки до определённого размера.

for file in *.jpg
do
	JPG=`basename "$file"`
	NAME="converted + $JPG"
	convert "$file" -resize 900 "$NAME"
done
