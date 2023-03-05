#!/bin/sh


# Скрипт был написан для архивирования электронных книг.
# Каждая книжка (файл) пакуется в «zip».
# Так как текстовый формат отлично сжимается -
# скрипт прекрасно позволяет экономить место на карте памяти моей электронной кнги.

for i in *.fb2 ;
do zip "$i".zip "$i" ;
   rm -f "$i" ;
done
