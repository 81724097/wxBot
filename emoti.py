#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ConfigParser
import base64
import json
from common import encode, decode

import requests

__author__ = 'Hang Yan'

BASE_URL = 'http://idc.emotibot.com/api/ApiKey/openapi.php'

USER_MAP_FILE = 'user.json'
USER_NAME_MAP = {}


def get_api_key():
    try:
        cf = ConfigParser.ConfigParser()
        cf.read('conf.ini')
        return cf.get('emoti', 'app_id')
    except Exception:
        pass


API_KEY = get_api_key()


def load_user_map():
    with open(USER_MAP_FILE, "r") as jsonFile:
        data = json.load(jsonFile)

    if data:
        global USER_NAME_MAP
        for k, v in data.iteritems():
            dk = decode(k)
            USER_NAME_MAP[dk] = v
            print '[LOAD-USER]: %s %s' % (dk, v)


def update_user_map(name, emoti_user_id):
    with open(USER_MAP_FILE, "r") as json_file:
        data = json.load(json_file)
    name_encode = encode(name)
    if not data.get(name_encode):
        data[name_encode] = emoti_user_id
        USER_NAME_MAP[name] = emoti_user_id
        print '[ADD-USER]: %s %s' % (name, emoti_user_id)

    with open(USER_MAP_FILE, "w") as json_file:
        json_file.write(json.dumps(data))


def reg_user():
    url = 'http://idc.emotibot.com/api/ApiKey/openapi.php'
    data = {
        'cmd': 'register',
        'appid': API_KEY
    }
    resp = requests.post(url, data=data).json()
    return resp['data'][0]['value']


def send_msg(user_name, msg):
    emoti_user_id = USER_NAME_MAP.get(user_name)
    if not emoti_user_id:
        emoti_user_id = reg_user()
        update_user_map(user_name, emoti_user_id)

    data = {
        'cmd': 'chat',
        'appid': API_KEY,
        'userid': emoti_user_id,
        'text': msg
    }

    resp = requests.post(BASE_URL, data=data).json()
    print json.dumps(resp)
    # print '情感: %s' % resp.get('emotion', [{}])[0].get('value')
    data_list = resp['data']
    return [x.get('value', '...') for x in data_list]
