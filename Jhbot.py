# -*- coding: utf-8 -*-

from ircmessage import IRCMessage
from setting import botnick,masterNick
from queue import Queue
import re
import threading
import time
from bojcrawl import BOJCrawler
from cfcrawl import CodeforcesCrawler, InitCFChangeList,CFRatingChange
from fibonacci import FibCalculator
from score import Sent, Score
from exchangecrawl import ExchangeCrawl, MakeNameDic, UpdateExDic, Exmsg

class Bot():
    irc = None
    msgQueue = Queue()
    exList = []
    nameDic = {}
    exDic = {}
    def __init__(self):
        from ircconnector import IRCConnector
        self.irc = IRCConnector(self.msgQueue)
        self.irc.setDaemon(True)
        self.irc.start()
        self.exList = ExchangeCrawl()
        self.nameDic = MakeNameDic(self.exList)
        self.exDic = UpdateExDic(self.exList, self.exDic)
        self.boj = BOJCrawler()
        self.cf = CodeforcesCrawler()
        self.fib = FibCalculator()

    def run(self):
        print('RUNNING')
        while True:
            packet = self.msgQueue.get()
            if packet['type'] == 'irc':
                message = packet['content']
                if message.msgType == 'INVITE':
                    print("%s invites to %s" % (message.sender, message.channel))
                    self.irc.joinchan(message.channel)

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
                        if command == '환율':
                            smsg = Exmsg(contents,self.exDic,self.nameDic)
                            self.irc.sendmsg(message.channel, smsg)
                            continue

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

                        if command == '코포':
                            msgs = self.cf.command(contents)
                            for msg in msgs:
                                self.irc.sendmsg(message.channel, msg)
                            continue

                    if message.msg.startswith('!치킨 '):
                        msgs = self.fib.chicken_command(message.msg[4:])
                        for msg in msgs:
                            self.irc.sendmsg(message.channel, msg)
                        continue

                    if message.msg.startswith('!fib '):
                        msgs = self.fib.fib_command(message.msg[5:])
                        for msg in msgs:
                           self.irc.sendmsg(message.channel, msg)
                        continue

                    parse = re.match(r'!백준\s+(\d+)$',message.msg)
                    if parse:
                        res = self.boj.command(parse.group(1))
                        for msg in res:
                            self.irc.sendmsg(message.channel, msg)
                        continue

                    if message.msg == '!환율':
                        self.irc.sendmsg(message.channel, 'ex)!환율 [숫자] <통화명> [-> <통화명>]')
                        continue

                    if message.msg == '!코포':
                        msgs = self.cf.command()
                        for msg in msgs:
                            self.irc.sendmsg(message.channel, msg)
                        continue

                    if message.msg == '부스터 옵줘':
                        self.irc.sendmode(message.channel,'+o ' + message.sender)
                        continue

                    if message.msg.find('치킨') != -1\
                            and message.msg.find('치킨') < message.msg.find('먹') < message.msg.find('싶'):
                        self.irc.sendmsg(message.channel, '치킨!')
                        continue

                    parse = re.search(r'부(우*)스터(어*)', message.msg)
                    if parse:
                        cry1 = len(parse.group(1))
                        cry2 = len(parse.group(2))
                        self.irc.sendmsg(message.channel, '크'\
                                + ('으'*cry1 if cry1 < 10 else '으*%d' % cry1)\
                                + ('아'*cry2 if cry2 < 10 else '아*%d' % cry2) + '앙')
                        continue

    def loopExCrawl(self):
        while True:
            time.sleep(5*60)
            self.exList = ExchangeCrawl()
            self.nameDic = MakeNameDic(self.exList)
            self.exDic = UpdateExDic(self.exList, self.exDic)

    def loopCFCrawl(self):
        RCList = InitCFChangeList('PJH0123')
        while True:
            time.sleep(5*60)
            newList = CFRatingChange('PJH0123',RCList)
            if newList:
                for i in range(max(len(newList)-2,0),len(newList)):
                    ch = newList[i]
                    RCList.append(ch['contestId'])
                    score = ch['newRating']-ch['oldRating']
                    score = chr(3) + ('12+' if score >= 0 else '07-') + str(abs(score)) + chr(3)
                    self.irc.sendmsg('#Jhuni', "[codeforeces] %s %d -> %d (%s) #%d at contest%d"\
                            % ('PJH0123', ch['oldRating'], ch['newRating'], score, ch['rank'], ch['contestId']))

    def start(self):
        threading.Thread(target = self.loopExCrawl, daemon = True).start()
        threading.Thread(target = self.loopCFCrawl, daemon = True).start()
        self.run()

if __name__ == '__main__':
    bot = Bot()
    bot.start()
