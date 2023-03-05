#!/bin/bash


# Перекодируем файлы .avi в .avi меньшего размера и для просмотра на телефоне
# Перекодируются все файлы с расширением avi в папке.
for file in *.avi
do
	AVI=`basename "$file"`
	NAME="2. + $AVI.mpg"
	# mencoder -oac mp3lame -lameopts  vbr=2:q=5  -ovc  lavc -lavcopts vcodec=mpeg4:mbd=2:vbitrate=850:keyint=250 -vf expand="320:240" -o "$NAME" "$file"
    ffmpeg -i "$file" "$NAME"
done
exit 0
