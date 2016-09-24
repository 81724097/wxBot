#!/usr/bin/env python
# coding: utf-8
import jandan

__author__ = 'iceke'
import requests
import json
import random
from bs4 import BeautifulSoup

UNKONWN = 'unkonwn'
SUCCESS = '200'
SCANED = '201'
TIMEOUT = '408'


def to_unicode(string, encoding='utf-8'):
    if isinstance(string, str):
        return string.decode(encoding)
    elif isinstance(string, unicode):
        return string
    else:
        raise Exception('Unknown Type')


def _get(url):
    try:
        response = requests.get(url)
        print 'Request: {}'.format(url)
        return response.json()
    except Exception as e:
        print 'Request exception: {}'.format(e)


def rec_film():
    way = random.randint(0, 5)
    message = ''
    if way <= 5:
        start = random.randint(1, 150)
        index = random.randint(1, 100)
        url = "https://api.douban.com/v2/movie/top250?start=" + str(start) + "&count=100"
        r = requests.get(url)
        data = json.loads(r.text)
        movie = data['subjects'][index]
        message += u"电影名称:" + movie['title'] + ',' + u"电影拍摄于" + movie['year'] + ',' + u"电影评分为:" + \
                   str(movie['rating']['average']) + u"。由" + movie['casts'][0]['name'] + ',' + \
                   movie['casts'][1][
                       'name'] + \
                   u"等演员主演。" + u"豆瓣链接:" + movie['alt'] + u"。 若不喜欢，可以回复换一部"
        return message


def rec_book():
    key = random.randint(1020561, 7020561)
    data = _get('https://api.douban.com/v2/book/{}'.format(key))
    if not data or not data.get('title'):
        return u'别看书了,去看片吧!'
    message = ''
    message += u'标题: %s\n' % data.get('title')
    message += u'作者: %s\n' % data.get('author', ['未知'])[0]
    message += u'简介: %s\n' % data.get('summary')
    message += u'链接: %s' % data.get('alt')
    return message


def rec_girls():
    key = random.randint(100, 2141)
    return 'http://jandan.net/ooxx/page-{}#comments'.format(key)


def rec_joke():
    return jandan.parse_joke()


def recommend_small_movie():
    url = "https://btso.pw/search/"
    r = requests.get(url, timeout=8)
    soup = BeautifulSoup(r.text, "html.parser")
    a_all = soup.find_all('a', class_='tag')
    fanhaos = []
    for a in a_all:
        fanhaos.append(a.get_text().split('.')[1])
        # print a
    index = random.randint(1, len(fanhaos) - 1)
    fanhao = fanhaos[index]
    print fanhao
    link = 'https://btso.pw/search/' + fanhao
    # print link
    r2 = requests.get(link, timeout=8)
    soup2 = BeautifulSoup(r2.text, "html.parser")

    magnet = []
    for a2 in soup2.find_all('a'):
        if 'hash' in a2.get('href'):
            magnet.append(a2.get('href'))
    if len(magnet) == 0:
        raise ValueError('magnet length is 0!')
    r3 = requests.get(magnet[0], timeout=8)
    soup3 = BeautifulSoup(r3.text, "html.parser")
    final_magnet = soup3.find('textarea').get_text().replace(';', '')
    message = u"不谢!番号是" + fanhao + u"。种子链接：" + final_magnet
    print  message
    return message


def rec_music():
    base = 'https://api.lostg.com/music'
    number = random.randint(1771052738, 1776052738)
    url = '{}/{}'.format(base, number)
    resp = requests.get(url)
    try:
        data = resp.json()
        str = u'专辑: %s\n' % data.get('album')
        str += u'歌手: %s\n' % data.get('singer')
        str += u'歌名: %s\n' % data.get('title')
        str += u'链接: %s\n' % 'http://www.xiami.com/song/{}'.format(number)
        return str
    except:
        number = random.randint(254601, 854601)
        url = '{}/163/songs/{}'.format(base, number)
        resp = requests.get(url)
        try:
            data = resp.json()
            str = u'专辑: %s\n' % data.get('album')
            str += u'歌手: %s\n' % data.get('singer')
            str += u'歌名: %s\n' % data.get('title')
            str += u'链接: %s\n' % 'http://music.163.com/#/song?id={}'.format(number)
            return str
        except:
            return u'不干!'


def rec_tec_art():
    base = 'https://hacker-news.firebaseio.com/v0'
    try:
        resp = requests.get('{}/topstories.json'.format(base))
        data = resp.json()
        l = len(data)
        number = data[random.randint(0, l - 1)]
        url = '{}/item/{}.json'.format(base, number)
        print "Tech Article: {}".format(url)
        res = requests.get(url)
        d = res.json()
        return '[{}] {}'.format(d.get('title'), d.get('url') or d.get('text'))
    except:
        return '哎呀,看什么技术文章啊,看个电影不好吗'


def rec_zhihu():
    base = 'http://news-at.zhihu.com/api'
    try:
        resp = requests.get('{}/3/news/hot'.format(base))
        data = resp.json()
        print data
        recent = data['recent']
        l = len(recent)
        item = recent[random.randint(0, l - 1)]
        print item
        url = item.get('url')
        real_url = requests.get(url).json().get('share_url')
        return '[%s] %s' % (item.get('title'), real_url)
    except Exception as e:
        print e
        return '别刷知乎了,快滚去学习!'



