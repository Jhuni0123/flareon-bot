# -*- coding: utf-8 -*-

from ircconnector import IRCConnector
from ircmessage import IRCMessage
from config import *
import re
import os
import threading
import time
from modules.bojcrawl import BOJCrawler
from modules.cfcrawl import CodeforcesCrawler, InitCFChangeList, CFRatingChange
from modules.fibonacci import FibCalculator
from modules.counter import Counter
from modules.xratecrawl import XRateCrawler

class Bot():
    def __init__(self, server, port):
        self.irc = IRCConnector(server, port)
        self.irc.init_user(botname)
        self.irc.set_nick(botnick)

        # init modules
        self.xrate = XRateCrawler()
        self.boj = BOJCrawler()
        self.cf = CodeforcesCrawler()
        self.fib = FibCalculator()
        self.counter = Counter()

        self.join_prevchan()
        self.botnames = self.getdb('botname')
        self.keywords = self.getdb('keyword')

    def run(self):
        while True:
            message = self.irc.get_next_msg()
            print(message)
            if message['command'] == 'INVITE':
                print("%s invites to %s" % (message['sender'], message['channel']))
                self.irc.joinchan(message['channel'])

            elif message['command'] == 'MODE':
                if message['mode'] == '+o' and message['users'][0] == botnick:
                    self.irc.send_msg(message['target'], '>ㅅ<')
                elif message['mode'] == '-o' and message['users'][0] == botnick:
                    self.irc.send_msg(message['target'], 'ㅇㅅㅇ..')

            elif message['command'] == 'PRIVMSG':
                if message['sender'] in botname:
                    continue
                parse = re.match(r'!(\S+)(?: (.*))?$',message['text'])
                if parse:
                    command = parse.group(1).lower()
                    text = parse.group(2)
                    result = None
                    if command in ['환율', 'xr']:
                        result = self.xrate.command(text)
                    elif command in ['점수', 'score']:
                        result = self.counter.command(text)
                    elif command in ['코포', 'cf']:
                        result = self.cf.command(text)
                    elif command == '치킨':
                        result = self.fib.chicken_command(text)
                    elif command == 'fib':
                        result = self.fib.fib_command(text)
                    elif command in ['백준', 'boj']:
                        result = self.boj.command(text)
                    if result != None:
                        for msg in result:
                            self.irc.send_msg(message['target'], msg)
                        continue

                called = False
                for keyword in self.keywords:
                    if message['text'].find(keyword) != -1:
                        called = True
                        break
                if called:
                    continue

                if message['text'] == '부스터 옵줘':
                    self.irc.set_mode(message['target'],'+o',[message['sender']])
                    continue

                if message['text'].find('치킨') != -1\
                        and message['text'].find('치킨') < message['text'].find('먹') < message['text'].find('싶'):
                    self.irc.send_msg(message['target'], '치킨!')
                    continue

                parse = re.search(r'부(우*)스터(어*)', message['text'])
                if parse:
                    cry1 = len(parse.group(1))
                    cry2 = len(parse.group(2))
                    self.irc.send_msg(message['target'], '크'\
                            + ('으'*cry1 if cry1 < 10 else '으*%d' % cry1)\
                            + ('아'*cry2 if cry2 < 10 else '아*%d' % cry2) + '앙')
                    continue

    def join_prevchan(self):
        chanlist = self.getdb('chanlist')
        for chan in chanlist:
            self.irc.join_chan(chan)

    def opendb(self, filename):
        dbdir = 'db/'
        if os.path.isdir(dbdir) == False:
            os.mkdir(dbdir)
        if not os.path.exists(dbdir + filename):
            file = open(dbdir + filename, 'w')
            file.close()
        file = open(dbdir + filename, 'r+')
        return file

    def getdb(self, filename):
        dbdir = 'db/'
        if os.path.isdir(dbdir) == False:
            os.mkdir(dbdir)
        if not os.path.exists(dbdir + filename):
            file = open(dbdir + filename, 'w')
            file.close()
        file = open(dbdir + filename, 'r+')
        db = []
        for line in file:
            db.append(line.strip())
        return db

    def loopExCrawl(self):
        while True:
            time.sleep(5*60)
            self.xrate.update()

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
                    self.irc.send_msg('#Jhuni', "[codeforeces] %s %d -> %d (%s) #%d at contest%d"\
                            % ('PJH0123', ch['oldRating'], ch['newRating'], score, ch['rank'], ch['contestId']))

    def start(self):
        threading.Thread(target = self.loopExCrawl, daemon = True).start()
        threading.Thread(target = self.loopCFCrawl, daemon = True).start()
        self.run()

if __name__ == '__main__':
    bot = Bot(server, port)
    bot.start()
