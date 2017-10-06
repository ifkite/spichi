# -*- coding: utf-8 -*-
'''
# =============================================================================
#      FileName: factory.py
#          Desc: a general factory which is used to generate other factories
#        Author: ifkite
#         Email: holahello@163.com
#      HomePage: http://github.com/ifkite
#      python version: 2.7.10
#    CreateTime: 2017-10-06 16:10:50
# =============================================================================
'''


class GeneralFactory(object):

    @staticmethod
    def gen():

        class Factory(object):
            backend_dict = {}
            def __init__(self, name):
                self.backend = self.backend_dict.get(name)
            def get_backend(self):
                return self.backend
            def build(self, *args, **kwargs):
                return self.backend(*args, **kwargs)

        return Factory
