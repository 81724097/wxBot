#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import random

__author__ = 'Hang Yan'

import urllib2

from bs4 import BeautifulSoup


def get_page_source(url):
    user_agent = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3'
    headers = {'User-Agent': user_agent}
    req = urllib2.Request(url, None, headers)
    response = urllib2.urlopen(req)
    page = response.read()
    response.close()
    return page


def get_soup(url):
    page = get_page_source(url)
    return BeautifulSoup(page)


def pick_one(items):
    l = len(items)
    return items[random.randint(0, l - 1)]


def _format_url(url):
    return url if url.startswith('http') else 'http:{}'.format(url)


def parse_girl_pic():
    url = 'http://jandan.net/ooxx'
    page = get_page_source(url)
    soup = BeautifulSoup(page)
    soup = soup.ol
    lis = soup.find_all('li')
    l = len(lis)
    picked = lis[random.randint(0, l - 1)]
    img = picked.find('img')
    src = _format_url(img['src'])
    filename = src.split('/')[-1]
    os.system("wget {} -P /tmp/".format(src))
    return '/tmp/{}'.format(filename)


def parse_man_pic():
    url = 'http://g.jandan.net/n/hanzi'
    page = get_page_source(url)
    soup = BeautifulSoup(page)
    imgs = soup.find_all('img', attrs={'class': 'img-limited'})
    l = len(imgs)
    picked = imgs[random.randint(0, l - 1)]
    src = _format_url(picked['src'])
    filename = '/tmp/{}'.format(src.split('/')[-1])
    os.system("wget {} -P /tmp/".format(src))
    return filename


def parse_joke():
    """From qiushibaike.com"""
    url = 'http://www.qiushibaike.com/hot/'
    soup = get_soup(url)
    items = soup.find_all('a', attrs={"target": "_blank", "class": "contentHerf"})
    item = pick_one(items)
    content = item.find('span').get_text()
    content.replace('<br/>', '\n')
    return content
