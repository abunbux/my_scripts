#!/bin/bash


# Перекодируем файлы .mp4 в .mp3.
# Перекодируются все файлы с расширением mp4 в папке.
for file in *.mp4
do
MP3=`basename "$file" ".mp4"`".mp3"
#Converting to mp3
`ffmpeg -i "$file" -vn -ar 44100 -ac 2 -ab 320k -f mp3 "$MP3"`
done
exit 0
# for file in *.webm
# do
# MP3=`basename "$file" ".webm"`".mp3"
# #Converting to mp3
# `ffmpeg -i "$file" -vn -ar 44100 -ac 2 -ab 320k -f mp3 "$MP3"`
# done
# exit 0
