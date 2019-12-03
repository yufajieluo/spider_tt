#!/usr/bin/python
#-*-coding:utf-8-*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
# copyright 2019 WShuai, Inc.
# All Rights Reserved.

# @File: commConfig.py
# @Author: WShuai, WShuai, Inc.
# @Time: 2019/11/29 16:34

import configparser

class OverrideConfigParser(configparser.ConfigParser):
    def __init__(self):
        configparser.ConfigParser.__init__(self)
        return
    def optionxform(self, optionstr):
        return optionstr

class CommConfig(object):

    def __init__(self, config_file):
        self.configger = OverrideConfigParser()
        self.configger.read(config_file)
        return

    def get_config(self):
        dict_config = {}
        for section in self.configger.sections():
            dict_config[section] = {}
            for key in self.configger.options(section):
                dict_config[section][key] = self.configger.get(section, key)
        return dict_config