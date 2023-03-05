#! /usr/bin/env python
# -*- coding: utf-8 -*-


import shutil
import os


list_dir = os.listdir()
for files in list_dir:
    dir_name, ext_mp3 = os.path.splitext(files)
    if ext_mp3 == '.mp3':
        os.mkdir(dir_name)
        # print(f'Создан каталог {dir_name}')
        shutil.move(files, dir_name)
        # print(f'Файл {files} перемещён в директорию {dir_name}.')
