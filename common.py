#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import string
import hashlib
import base64

__author__ = 'Hang Yan'


def rand_low_str(length, upper=False, lower=True, digit=False, punc=False):
    choice = ''
    if upper:
        choice += string.ascii_uppercase
    if lower:
        choice += string.ascii_lowercase
    if digit:
        choice += string.digits
    if punc:
        choice += string.punctuation
    if not choice:
        return choice
    return ''.join(random.choice(choice) for _ in range(length))


# def md5(data):
#     m = hashlib.md5()
#     m.update(data.encode('utf-8') if type(data) == unicode or data)
#     return m.hexdigest()


def encode(data):
    if type(data) == unicode:
        return base64.b64encode(data.encode('utf-8'))
    return base64.b64encode(data)


def decode(data):
    return base64.b64decode(data).decode('utf-8')


