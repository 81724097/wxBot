#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import string

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
