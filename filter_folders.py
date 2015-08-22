#! /usr/bin/env python

import os

prefix = '/Users/Shared/Photo Library/'
dirs = set()
with open('file_list.txt') as allFiles:
    for i, file in enumerate(allFiles):
        dirs.add(prefix + file.rsplit('/', 1)[0])

directories = list(dirs)
directories.sort()

with open('path_list.txt', 'w') as allPaths:
    for i in directories:
        allPaths.write(i + '\n')
