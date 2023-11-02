"""

@author = ANIKET YADAV
"""

import os


def route(file_name, dir_name='biobeee'):
    PATH = ''
    PATH_DIR = ''
    for root, dir, files in os.walk(f'{os.getcwd()[0]}:/'):
        for f in files:
            if f == file_name:
                PATH += os.path.join(root, f)
        for d in dir:
            if d == dir_name:
                PATH_DIR += os.path.join(root, d)
    return PATH.replace('\\', '/'), PATH_DIR.replace('\\', '/')


# print(route('ebiBee.py'))