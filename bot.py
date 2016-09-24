#!/usr/bin/env python
# coding: utf-8
import jandan
from recomend import rec_zhihu
from wxbot import *
import ConfigParser
import json
import recomend


class TulingWXBot(WXBot):
    def __init__(self):
        WXBot.__init__(self)

        self.tuling_key = ""
        self.switch = {}

        try:
            cf = ConfigParser.ConfigParser()
            cf.read('conf.ini')
            self.tuling_key = cf.get('main', 'key')
        except Exception:
            pass
        print 'tuling_key:', self.tuling_key

    def tuling_auto_reply(self, uid, msg):
        if self.tuling_key:
            url = "http://www.tuling123.com/openapi/api"
            user_id = uid.replace('@', '')[:30]
            body = {'key': self.tuling_key, 'info': msg.encode('utf8'), 'userid': user_id}
            r = requests.post(url, data=body)
            respond = json.loads(r.text)
            result = ''
            if respond['code'] == 100000:
                result = respond['text'].replace('<br>', '  ')
            elif respond['code'] == 200000:
                result = respond['url']
            elif respond['code'] == 302000:
                for k in respond['list']:
                    result = result + u"【" + k['source'] + u"】 " + \
                             k['article'] + "\t" + k['detailurl'] + "\n"
            elif respond['code'] == 308000:
                for k in respond['list']:
                    result += '[%s] %s %s \n' % (k['name'], k['info'], k['detailurl'])
            else:
                result = respond['text'].replace('<br>', '  ')

            print '    ROBOT:', result
            return result
        else:
            return u"知道啦"

    @staticmethod
    def append_map(words, value, to_dict):
        for word in words:
            to_dict[word] = value

    def append_all(self, to):
        self.append_map([
            u'唱首歌',
            u'推荐首歌',
            u'唱歌'
        ], 'rec_music', to)

        self.append_map([
            u'讲个段子',
            u'来个段子',
            u'说个段子'
        ], 'rec_joke', to)

    def rec(self, msg, user_id):
        REC_MAP = {
            u'推荐歌曲': 'rec_music',
            u'技术文章': 'rec_tec_art',
            u'推荐电影': 'rec_film',
            u'推荐书': 'rec_book',
            u'美女图': 'rec_girls',
            u'段子': 'rec_joke'
        }
        self.append_all(REC_MAP)

        PIC_REC_MAP = {
            u'妹子': 'parse_girl_pic',
            u'汉子': 'parse_man_pic'
        }
        self.append_map([
            u'帅哥',
            u'肌肉男',
            u'男神'
        ], 'parse_man_pic', PIC_REC_MAP)

        for k, v in REC_MAP.iteritems():
            if k == msg:
                return self.send_msg_by_uid(getattr(recomend, v)(), user_id)

        for k, v in PIC_REC_MAP.iteritems():
            if k == msg:
                filename = getattr(jandan, v)()
                res = self.send_image(filename, user_id)
                os.remove(filename)
                return res
        return False

    def handle_msg_all(self, msg):
        # text message from contract
        if msg['msg_type_id'] == 4 and (msg['content']['type'] == 0 or msg['content']['type'] == 6):
            print "Message from contract : %s" % msg['user']['name']
            if msg['content']['type'] == 6:
                self.send_random_emoji(msg['user']['id'])
                return
            # 处理聊天逻辑
            if self.rec(msg['content']['data'], msg['user']['id']):
                return
            self.send_msg_by_uid(self.tuling_auto_reply(msg['user']['id'], msg['content']['data']),
                                 msg['user']['id'])

        # group message
        elif msg['msg_type_id'] == 3 and msg['content']['type'] in [0, 3, 4, 6, 12]:
            print "Group Message: %s -> %s" % (msg['user']['name'], msg['content']['user']['name'])

            gid = msg['user']['id']

            # check switch
            if 'detail' in msg['content']:
                desc = msg['content'].get('desc')
                if desc in [u'退下', u'滚', u'渣渣']:
                    self.switch[gid] = False
                    self.send_msg_by_uid(u'走了!', msg['user']['id'])
                    return
                if desc in [u'回来', u'出来', u'粗来']:
                    self.switch[gid] = True
                    self.send_msg_by_uid(u'来了!', msg['user']['id'])
                    return

            if not self.switch.get(gid, False):
                print "Robot is off!"
                return

            # emoji message
            if msg['content']['type'] == 6:
                self.send_random_emoji(msg['user']['id'])
                return

            # 处理新拉入群操作
            if msg['content']['is_entergroup'] == 1:
                reply = u'各位好，我是长者。'
                reply += u'我的功能有：1.艾特我，我会和你对话； 2.在群聊中进行随机说话； 3.可以咨询天气或者部分词条，回复推荐电影，推荐豆瓣电影，回复我要看片，推荐老司机电影；' \
                         u'4.支持群聊天消息撤回的重发，包括文字，图片，语音，暂不支持表情；5.回复艾特全员，自动帮你艾特全部群成员；6.当有红包消息时，自动艾特所有群成员进行提醒'
                self.send_msg_by_uid(reply, msg['user']['id'])
                return

            # 处理红包
            if msg['content']['is_hongbao'] == 1:
                reply = u'有人发红包啦！！ '
                for member_name in self.get_all_group_member_name(msg['user']['id']):
                    reply += '@' + member_name + ' '
                self.send_msg_by_uid(reply, msg['user']['id'])
                return

            # 处理艾特全员逻辑
            if u'艾特' in msg['content'].get('desc') and u'全员' in msg['content'].get('desc'):
                reply = ''
                reply1 = ''
                reply2 = ''
                reply3 = ''
                reply4 = ''
                reply5 = ''
                a = ('2005',)
                print '@' + "member" + ('\\u%s' % a).decode('unicode-escape')
                for member_name in self.get_all_group_member_name(msg['user']['id']):
                    reply += u'@' + member_name + u'\u2005' + ' '
                    reply1 += '@' + u'\u2005' + member_name + ' '
                    reply2 += '@' + member_name + ('\\u%s' % a).decode('unicode-escape')
                    reply3 += '@' + member_name + '\u2005'.decode('unicode-escape')
                    reply4 += '@' + '\u2005'.decode('unicode-escape') + member_name
                    reply5 += '@' + '\\u2005'.decode('unicode-escape') + member_name

                self.send_msg_by_uid(reply, msg['user']['id'])

                return

            # 处理文本消息
            if 'detail' in msg['content']:
                my_names = self.get_group_member_name(msg['user']['id'], msg['to_user_id'])
                if my_names is None:
                    my_names = {}
                if 'NickName' in self.my_account and self.my_account['NickName']:
                    my_names['nickname2'] = self.my_account['NickName']
                if 'RemarkName' in self.my_account and self.my_account['RemarkName']:
                    my_names['remark_name2'] = self.my_account['RemarkName']

                is_at_me = False

                for detail in msg['content']['detail']:
                    if detail['type'] == 'at':
                        for k in my_names:
                            if my_names[k] and my_names[k] == detail['value']:
                                is_at_me = True
                                break

                if is_at_me:
                    src_name = msg['user']['name']
                    reply = '@' + src_name + ': '
                    if msg['content']['type'] == 0:  # text message
                        reply += self.tuling_auto_reply(msg['content']['user']['id'],
                                                        msg['content']['desc'])
                    else:
                        reply += u"对不起，只认字，其他杂七杂八的我都不认识，,,Ծ‸Ծ,,"
                    self.send_msg_by_uid(reply, msg['user']['id'])

                if is_at_me is False:
                    # src_name = msg['user']['name']
                    reply = ''
                    if self.rec(msg['content']['desc'], msg['user']['id']):
                        return
                    if u'耿老师' in msg['content']['desc']:
                        return self.send_msg_by_uid(u'耿老师最瘦最萌!', msg['user']['id'])
                    if u'知乎' in msg['content']['desc']:
                        return self.send_msg_by_uid(rec_zhihu(), msg['user']['id'])
                    if msg['content']['type'] == 0:  # text message
                        reply += self.tuling_auto_reply(msg['content']['user']['id'],
                                                        msg['content']['desc'])
                    else:
                        reply += u"我很想知道你说的什么"
                    print u"主动发言:" + reply
                    self.send_msg_by_uid(reply, msg['user']['id'])


def main():
    bot = TulingWXBot()
    bot.DEBUG = True
    bot.conf['qr'] = 'tty'

    bot.run()


if __name__ == '__main__':
    main()
