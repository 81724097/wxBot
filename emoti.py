#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ConfigParser

__author__ = 'Hang Yan'


def get_api_key():
    try:
        cf = ConfigParser.ConfigParser()
        cf.read('conf.ini')
        self.tuling_key = cf.get('emoti', 'key')
    except Exception:
        pass
    print 'tuling_key:', self.tuling_key


def reg_user(user_id):
