# -*- coding: utf-8 -*-
'''
# =============================================================================
#      FileName: utils.py
#          Desc: 
#        Author: ifkite
#         Email: holahello@163.com
#      HomePage: http://github.com/ifkite
#      python version: 2.7.10
#    LastChange: 2017-06-27 07:22:02
# =============================================================================
'''
from hashlib import sha1
from random import random
from time import time


def get_path_info(environ):
    from urllib import quote
    path_info = quote(environ.get('PATH_INFO',''),safe='/;=,')
    if not environ.get('SCRIPT_NAME'):
        return path_info[1:]
    else:
        return path_info


def time_text():
    return str(time()).encode('ascii')


def random_text():
    # PY2
    return unicode(random()).encode('ascii')


def generate_key(salt=None):
    return sha1(b''.join([
        salt,
        time_text(),
        random_text(),
        ])).hexdigest()
