# -*- coding: utf-8 -*-

from ircconnector import IRCConnector
from ircmessage import IRCMessage
from config import *
import re
import threading
import time
from bojcrawl import BOJCrawler
from cfcrawl import CodeforcesCrawler, InitCFChangeList,CFRatingChange
from fibonacci import FibCalculator
from counter import Counter
from exchangecrawl import ExchangeCrawl, MakeNameDic, UpdateExDic, Exmsg

class Bot():
    exList = []
    nameDic = {}
    exDic = {}
    def __init__(self, server, port):
        self.irc = IRCConnector(server, port)
        self.irc.init_user(botname)
        self.irc.set_nick(botnick)
        self.exList = ExchangeCrawl()
        self.nameDic = MakeNameDic(self.exList)
        self.exDic = UpdateExDic(self.exList, self.exDic)
        self.boj = BOJCrawler()
        self.cf = CodeforcesCrawler()
        self.fib = FibCalculator()
        self.counter = Counter()

        self.irc.join_chan('#jhuni-bot-test')

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
                parse = re.match(r'!(\S+)(?: (.*))?$',message['text'])
                if parse:
                    command = parse.group(1)
                    text = parse.group(2)
                    result = []
                    if command == '환율':
                        if text == None:
                            result.append('ex)!환율 [숫자] <통화명> [-> <통화명>]')
                        else:
                            smsg = Exmsg(text,self.exDic,self.nameDic)
                            result.append(smsg)
                    elif command == '점수' or command == 'score':
                        result = self.counter.command(text)
                    elif command == '코포':
                        result = self.cf.command(text)
                    elif command == '치킨':
                        result = self.fib.chicken_command(text)
                    elif command == 'fib':
                        result = self.fib.fib_command(text)
                    elif command == '백준':
                        result = self.boj.command(text)
                    for msg in result:
                        self.irc.send_msg(message['target'], msg)

                if message['text'] == '부스터 옵줘':
                    self.irc.mode(message['target'],'+o ' + message['sender'])
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
                    self.irc.send_msg('#Jhuni', "[codeforeces] %s %d -> %d (%s) #%d at contest%d"\
                            % ('PJH0123', ch['oldRating'], ch['newRating'], score, ch['rank'], ch['contestId']))

    def start(self):
        threading.Thread(target = self.loopExCrawl, daemon = True).start()
        threading.Thread(target = self.loopCFCrawl, daemon = True).start()
        self.run()

if __name__ == '__main__':
    bot = Bot(server, port)
    bot.start()
