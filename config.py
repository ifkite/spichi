# -*- coding: utf-8 -*-
'''
# =============================================================================
#      FileName: config.py
#          Desc: 
#        Author: ifkite
#         Email: holahello@163.com
#      HomePage: http://github.com/ifkite
#      python version: 2.7.10
#    LastChange: 2017-07-30 12:00:09
# =============================================================================
'''

import imp
import json
import os


class Config(dict):
    __slot__ = ['__dict__', 'from_json', 'from_pyfile']

    def __init__(self, path):
        self.path = path
        self.module_name = 'spichi_config'

    def from_json(self, filename):
        fullpath = os.path.join(self.path, filename)

        with open(fullpath, 'rb') as json_filename:
            config_dict = json.loads(json_filename.read())

        for k,v in config_dict.iteritems():
            if k.isupper():
                self[k] = v

    def from_pyfile(self, filename):
        # importlib.import_module

        py_file, py_path, py_desc = imp.find_module(filename, [self.path])
        py_module = imp.load_module(filename, py_file, py_path, py_desc)
        py_file.close()
        self.update_config(py_module)

    def update_config(self, conf):

        for k in dir(conf):
            if k.isupper():
                self[k] = getattr(conf, k)
