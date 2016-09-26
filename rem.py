#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

__author__ = 'Hang Yan'

import os

REM_FILE = 'rem.json'


def parse_remind_info(msg):
    if not msg.starts(u'提醒我'):
        return

    t = msg[3:8]
    stuff = msg[8:]
    return {
        'time': t,
        'stuff': stuff
    }


def save_remind_info():
    with open(REM_FILE, "w+") as f:
        data = json.load(f)
    if data:
        