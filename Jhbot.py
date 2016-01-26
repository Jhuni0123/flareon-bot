# -*- coding: utf-8 -*-

from ircmessage import IRCMessage
from setting import botnick
from queue import Queue
from score import Sent, Score
from chib import fib, Chib, EE, Bi, Mkbi, Mkd
import re
from bojcrawl import BOJCrawl
from cfcrawl import CFCrawl
class Bot():
    irc = None
    msgQueue = Queue()
    channel_list = []

    def __init__(self):
        from ircconnector import IRCConnector
        self.irc = IRCConnector(self.msgQueue)
        self.irc.setDaemon(True)
        self.irc.start()

    def run(self):
        while True:
            packet = self.msgQueue.get()
            if packet['type'] == 'msg':
                msg = packet['content']
                for channel in self.channel_list:
                    self.irc.sendmsg(channel, msg)

            elif packet['type'] == 'irc':
                message = packet['content']
                print(message)
                if message.msgType == 'INVITE':
                    self.irc.joinchan(message.channel)

                elif message.msgType == 'NOTICE':
                    if message.sender == 'Jhuni' and message.channel == botnick:
                        self.irc.semdmsg('#snucse16',message.msg)
                        continue
                elif message.msgType == 'MODE':
                    if message.msg == '+o ' + botnick:
                        self.irc.sendmsg(message.channel, '>ㅅ<')
                    elif message.msg == '-o ' + botnick:
                        self.irc.sendmsg(message.channel, 'ㅇㅅㅇ..')

                elif message.msgType == 'PRIVMSG':
                    parse = re.match(r'!(\S+)\s+(.*)$',message.msg)
                    if parse:
                        command = parse.group(1)
                        contents = parse.group(2)
                        if command == '점수' or command == 'score':
                            sen = Sent(contents)
                            if sen == '':
                                self.irc.sendmsg(message.channel, "적절하지 않은 영단어입니다")
                                continue
                            scr = Score(sen)
                            if scr == 100:
                                self.irc.sendmsg(message.channel, "'%s'은(는) %d점짜리 입니다" % (contents,scr))
                                continue
                            else:
                                self.irc.sendmsg(message.channel, "'%s'은(는) %d점" % (contents, scr))
                                continue
                    parse = re.match(r'!치킨\s+(\d+)\s*(\S*)',message.msg)
                    if parse:
                        num = int(parse.group(1))
                        etc = parse.group(2)
                        if etc == '명' or etc == '':
                            if num == 1:
                                self.irc.sendmsg(message.channel, '1인1닭은 진리입니다')
                                continue
                            elif num == 2:
                                self.irc.sendmsg(message.channel, '계산상 1마리지만 1인1닭에 따라 2마리가 적절합니다')
                                continue
                            elif num >= 573147844013817084101:
                                self.irc.sendmsg(message.channel, '필요한 치킨이 너무 많아 셀 수 없습니다')
                                continue
                            else:
                                self.irc.sendmsg(message.channel, '%d명에게는 %d마리의 치킨이 적절합니다' % (num, Chib(int(num))))
                            if num == 12117:
                                self.irc.sendmsg(message.channel, 'gs12117에게는 0.5마리의 치킨이면 충분합니다')
                            if EE(num):
                                self.irc.sendmsg(message.channel, '%d명에게는 %d마리의 치킨이 적절합니다' % (num, Chib(int(num))))
                            if Bi(num):
                                self.irc.sendmsg(message.channel, '%s명에게는 %s마리의 치킨이 적절합니다' % (Mkbi(Mkd(num)), Mkbi(Chib(int(Mkd(num))))))
                            continue

                    if message.msg.find('치킨') != -1 and message.msg.find('치킨') < message.msg.find('먹') < message.msg.find('싶'):
                        self.irc.sendmsg(message.channel, '치킨!')
                        continue
                    parse = re.match(r'!fib\s+(-?\d+)$',message.msg)
                    if parse:
                        num = int(parse.group(1))
                        if num > 256:
                            self.irc.sendmsg(message.channel, '[fib] result is too big')
                        elif num < 0:
                            self.irc.sendmsg(message.channel, '[fib] incorrect input')
                        else:
                            self.irc.sendmsg(message.channel, '[fib] %d' % fib[num])
                        continue
                    parse = re.match(r'!백준\s+(\d+)$',message.msg)
                    if parse:
                        num = int(parse.group(1))
                        url = 'https://www.acmicpc.net/problem/%d' % num
                        title = BOJCrawl(url)
                        if title:
                            self.irc.sendmsg(message.channel, title + ' - ' + 'https://icpc.me/%d' % num)
                        else:
                            self.irc.sendmsg(message.channel, 'Not found')
                        continue
                    if message.msg == '!코포':
                        contestlist = CFCrawl()
                        for con in contestlist:
                            self.irc.sendmsg(message.channel, '[%s]%s/%s/%s' % (con[0],con[1],con[2],con[3]))
                        continue
                    if message.msg.find('부스터') != -1:
                        self.irc.sendmsg(message.channel, '크앙')

if __name__ == '__main__':
    bot = Bot()
    bot.run()
