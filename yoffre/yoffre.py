#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 abunbux <abunbux@pasha>
#
# Distributed under terms of the MIT license.
#
# Перекодирует и переименовывает файлы.
# В качестве аргументов принимает:
# '-d' ('--directory') - принимает папку с обрабатываемыми файлами, если он не указан - то используется
# папка, откуда запускается скрипт.
# '-e' ('--extension') - указывает на расширение обрабатываемых файлов.
# '-r' ('--recursively') - работает рекурсивно.
#
# подпрограмма 'rename' - переименовать файлы (для файлов, скачанных с yotube программой yotube-dl).
# Перед началом обработки, в консоль нужно вывести файлы со старым и новым именами и запросить у пользователя
# подтверждения на действия.
# '-y' ('--yes') - пропускает вывод файлов в консоль и сразу обрабатывает.
#
# подпрограмма 'ffmpeg' - перекодировать файлы (использует установленный в системе ffmpeg).
# Производится проверка на наличие в системе ffmpeg. Если нет - уведомление пользователю.
# '-vn' - не кодировать видео
# '-f' - выходящий формат (расширение после обработки).
# '-ab' - аудиобитрейт.
# '-ar' - частота дискретизации.
# '-ac' - количество аудиоканалов.
#
# Аргумент '--version' - показывает версию скрипта.
# Также реализована проверка имён с помощью модуля re, дабы не испортить имена файлов в этом не нуждающихся.
# Имена, длина которых меньше или равна 12-ти символам, не обрабатываются.
# Если в папке нет файлов с нужным расширением - делает выход с уведомлением.
#

import subprocess
import os
import sys
import argparse
import re

version = "1.0.0"
FFMPEG = 'ffmpeg'
prog = 'yoffre'

pattern_date = re.compile(r'[-\s()]{,}\d+\.\d+\.\d+', re.DOTALL | re.VERBOSE)
pattern_youtube = re.compile(r'-\b[\w\d]+[^а-яА-Я]\b', re.DOTALL | re.VERBOSE)


# Возвращает парсер с подпарсерами для обработки аргументов командной строки.
def create_parser():
    parser = argparse.ArgumentParser(prog=prog,
                                     description='''Переименовывает файлы,
                                     скачанные утилитой youtube-dl, а также перекодирует
                                      в аудиоформаты, используя ffmpeg''',
                                     epilog='(c) abunbux 18.10.2015')
    parser.add_argument('--version', action='version', help='Вывести номер версии',
                        version='%(prog)s {}'.format(version))

    subparsers = parser.add_subparsers(dest='command')

    ffmpeg_parser = subparsers.add_parser('ffmpeg')
    ffmpeg_parser.add_argument('-r', '--recursively', action='store_true', help='Рекурсивная обработка')
    ffmpeg_parser.add_argument('-d', '--directory', default=os.getcwd(),
                               help='''Укажите директорию с обрабатываемыми файлами,
                               по-умолчанию таковой будет считаться директория, откуда запускается скрипт.''')
    ffmpeg_parser.add_argument('-e', '--extension',
                               help='''Укажите расширение обрабатываемых файлов. Этот параметр обязателен.''')
    ffmpeg_parser.add_argument('-y', '--yes', action='store_true',
                               help='''Указание параметра даёт предварительное согласие на обработку файлов
                               без просмотра их в виде списка. Если параметр не указан, в консоль будет выведен
                               список обрабатываемых файлов и запрос на дальнейшие действия.''')
    ffmpeg_parser.add_argument('-vn', action='store_true', default=True, help='Не кодировать видео.')
    ffmpeg_parser.add_argument('-f', default='mp3', help='Требуемый выходящий формат.')
    ffmpeg_parser.add_argument('-ab', default='96k', help='Битрейт аудио.')
    ffmpeg_parser.add_argument('-ar', default='44100', help='Частота дискретизации.')
    ffmpeg_parser.add_argument('-ac', default='2', help='Количество аудиоканалов.')
    ffmpeg_parser.add_argument('--rename', action='store_true',
                               help='Переименовать файлы.')

    rename_parser = subparsers.add_parser('rename')
    rename_parser.add_argument('-r', '--recursively', action='store_true', help='Рекурсивная обработка')
    rename_parser.add_argument('-d', '--directory', default=os.getcwd(),
                               help='''Укажите директорию с обрабатываемыми файлами, по-умолчанию таковой будет
                               считаться директория, откуда запускается скрипт.''')
    rename_parser.add_argument('-e', '--extension',
                               help='''Укажите расширение обрабатываемых файлов вместе с точкой.
                               Этот параметр обязателен.''')
    rename_parser.add_argument('-y', '--yes', action='store_true',
                               help='''Указание параметра даёт предварительное согласие на обработку файлов
                               без просмотра их в виде списка. Если параметр не указан, в консоль будет выведен
                               список обрабатываемых файлов и запрос на дальнейшие действия.''')
    rename_parser.add_argument('--ffmpeg', action='store_true', help='Перекодировать файлы.')

    return parser


# Возвращает словарь для подпрограммы 'rename', где в качестве ключа фигурирует старое имя файла, а в качестве
# значения - новое имя. Аргументами в функцию передаются путь к папке (namespace.directory) - по умолчанию равен папке,
# откуда запускается скрипт, и расширение обрабатываемых файлов (namespace.extension) - указывать обязательно.
def build_dict_rename(path, ext):
    list_dir = os.listdir(path)
    ext = '.' + ext
    work_dict = {}
    for files in list_dir:
        name, extansion = os.path.splitext(files)
        if extansion == ext and len(name) >= 12:
            if name[-12] == '-' and not pattern_date.search(name[-12:]) and pattern_youtube.search(name[-12:]):
                oldname = files
                newname = (name[:-12]).strip('\n.,') + extansion
                work_dict[os.path.join(path, oldname)] = os.path.join(path, newname)
    # print(work_dict)
    return work_dict


# Возвращает рекурсивный словарь для подпрограммы 'rename', где в качестве ключа фигурирует старое имя файла,
# а в качестве значения - новое имя. Аргументами в функцию передаются путь к папке (namespace.directory)
# - по умолчанию равен папке, откуда запускается скрипт, и расширение обрабатываемых файлов (namespace.extension) -
# указывать обязательно.
def build_dict_recursively_rename(path, ext):
    list_dir = os.walk(path)
    ext = '.' + ext
    work_dict = {}
    for pathes, dirs, files in list_dir:
        for file in files:
            work_file = pathes + os.path.sep + file
            name, extansion = os.path.splitext(work_file)
            if extansion == ext:
                if name[-12] == '-' and not pattern_date.search(name[-12:]) and pattern_youtube.search(name[-12:]):
                    oldname = work_file
                    newname = (name[:-12]).strip() + extansion
                    work_dict[os.path.join(path, oldname)] = os.path.join(path, newname)
    # print(work_dict)
    return work_dict


# Возвращает список для подпрограммы 'ffmpeg', который содержит все файлы с указанным расширением.
# Аргументами в функцию передаются путь к папке (namespace.directory)  - по умолчанию равен папке,
# откуда запускается скрипт, и расширение обрабатываемых файлов (namespace.extension) - указывать обязательно.
def build_dict_ffmpeg(path, ext):
    list_dir = os.listdir(path)
    ext = '.' + ext
    work_list = []
    for files in list_dir:
        name, extansion = os.path.splitext(files)
        if extansion == ext:
            name = name.strip('\n.,-') + extansion
            work_list.append(os.path.join(path, name))
    return work_list


# Возвращает рекурсивный список для подпрограммы 'ffmpeg', который содержит все файлы с указанным расширением.
# Аргументами в функцию передаются путь к папке (namespace.directory)  - по умолчанию равен папке,
# откуда запускается скрипт, и расширение обрабатываемых файлов (namespace.extension) - указывать обязательно.
def build_dict_recursively_ffmpeg(path, ext):
    list_dir = os.walk(path)
    ext = '.' + ext
    work_list = []
    for pathes, dirs, files in list_dir:
        for file in files:
            work_file = pathes + os.path.sep + file
            name, extansion = os.path.splitext(work_file)
            if extansion == ext:
                # oldname = work_file
                newname = name.strip() + extansion
                work_list.append(os.path.join(path, newname))
    return work_list


# Выводит на экран список обрабатываемых файлов для подтверждения дальнейшей обработки.
# Используется обеими подпрограммами - и 'rename' и 'ffmpeg'.
# В качестве аргумента может принимать словарь или список, построенные ранее функциями:
# 'build_dict_rename', 'build_dict_recursively_rename' для 'rename'
# или 'build_dict_ffmpeg', 'build_dict_recursively_ffmpeg' для 'ffmpeg'
def show_work_dict_list(work_dict_list):
    if isinstance(work_dict_list, dict):
        for key in sorted(work_dict_list):
            print(os.path.basename(key), ' => ', os.path.basename(work_dict_list[key]))
            # print(os.path.basename(work_dict[key]))
    elif isinstance(work_dict_list, list):
        for file in work_dict_list:
            print(os.path.basename(file))
    print()


# Переименовывает обрабатываемые файлы и выводит результат работы на экран.
# В качестве аргумента принимает словарь от функций 'build_dict_rename' или 'build_dict_recursively_rename'.
def renamer(work_dict):
    for key, value in work_dict.items():
        print(os.path.basename(value))
        os.rename(key, value)


# Перекодирует обрабатываемые файлы и выводит результат на экран.
# В качестве аргументов принимает словарь от функций 'build_dict_ffmpeg' или 'build_dict_recursively_ffmpeg',
# а также namespace.ar, namespace.ac, namespace.ab, namespace.f
def codingffmpeg(work_list, ar, ac, ab, f):
    for file in work_list:
        name, extansion = os.path.splitext(file)
        newname = name + '.' + f
        subprocess.call([FFMPEG, '-i', file, '-vn', '-ar', ar, '-ac', ac, '-ab', ab, '-f', f, newname])
        print(os.path.basename(file), ' = ', os.path.basename(newname))


def answers(function, *args):
    answer = input('Продолжить или прекратить? (Y/y or N/n)')
    print()
    if answer == 'Y' or answer == 'y' or answer == '':
        function(*args)
    else:
        print()
        print('Ну да ладно, до скорого свидания.')
        sys.exit(0)


def if_empty(work_dict_list):
    if not work_dict_list:
        print('Обрабатывать нечего - выходим.')
        sys.exit(0)


def main():
    parsers = create_parser()
    namespace = parsers.parse_args()
    # Если не указана ни одна из подпрограмм - на экран выводится ошибка и подсказка для пользователя.
    # Если не указано расширение и подпрограммы - выводится на экран ошибка и подсказка.
    if namespace.command is None:
        parsers.error('''Необходимо указать подпрограмму.
        Используйте "{0} ffmpeg --help" или "{0} rename --help" для получения справки.'''.format(prog))
    elif namespace.command is not None and namespace.extension is None:
        parsers.error('''Необходимо указать расширение.
        Используйте "{0} ffmpeg --help" или "{0} rename --help" для получения справки.'''.format(prog))

    # Здесь начинается поле деятельности подпрограммы 'rename'.
    if namespace.command == 'rename':
        if namespace.recursively:
            work_dict = build_dict_recursively_rename(namespace.directory, namespace.extension)
        else:
            work_dict = build_dict_rename(namespace.directory, namespace.extension)
        if_empty(work_dict)
        if namespace.yes is False:
            show_work_dict_list(work_dict)
            answers(renamer, work_dict)
        else:
            renamer(work_dict)

    # Дальше работает 'ffmpeg'.
    elif namespace.command == 'ffmpeg':
        if namespace.recursively:
            work_list = build_dict_recursively_ffmpeg(namespace.directory, namespace.extension)
        else:
            work_list = build_dict_ffmpeg(namespace.directory, namespace.extension)
        if_empty(work_list)
        if namespace.yes is False:
            show_work_dict_list(work_list)
            answers(codingffmpeg, work_list, namespace.ar, namespace.ac, namespace.ab, namespace.f)
        else:
            codingffmpeg(work_list, namespace.ar, namespace.ac, namespace.ab, namespace.f)

    else:
        parsers.print_help()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print()
        print('Программа завершена пользователем.')
        sys.exit(0)
