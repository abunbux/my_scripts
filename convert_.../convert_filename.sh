#!/bin/bash


# Конвертация имён файлов и каталогов из заданной кодировки в текущую
if [ "$1" = ""]
then echo "Исходная кодировка не указана! Пожалуйста укажите кодировку, например cp1251 или koi8-r"; exit 1
fi
PWD=$(pwd) # Запоминаем текущий каталог
# Ищем все вложенные каталоги в текущем и отдаём их переменной цикла и временно
# заменяем пробелы в названиях на \ для исключения проблем с восприятием одного имени файла как нескольких.
for i in $(find $PWD -type d -depth | sed 's/ /\\/g')
do
    #Возвращяем пробелы в имена файлов и каталогов и запоминаем в переменной dest
    dest=$(echo "$i" | sed 's/\\/ /g')
    cd "$dest" #Переходим в каталог
    #Конвертируем имена содержимого катаога  из заданной кодировки в текущую
    for n in *
    do
        conv=$(echo "$n" | iconv -c -f "$1")
        mv "$n" "$conv"
    done
    cd $PWD
done
