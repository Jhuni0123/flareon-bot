# -*- coding: utf-8 -*-

from ircmessage import IRCMessage
from setting import botnick,masterNick
from queue import Queue
from score import Sent, Score
from chib import fib, Chib, EE, Bi, Mkbi, Mkd
import re, threading, time
from bojcrawl import BOJCrawl
from cfcrawl import CFContestList,CFUserInfo,InitCFChangeList,CFRatingChange
from exchangecrawl import ExchangeCrawl, MakeNameDic, UpdateExDic, Exmsg

callNameList = ['마폭시','큐베러버','참치','브랸','브리안','브리얀','젠카이노','!폭렬','!확률','!토픽']
botNameList = [r'\b','C','bryan_a','cube1over','VBChunguk_bot','gn','kcm1700-bot','치즈','Diet-bot','JW270','Bonobot','B','Delphox','Draco','﻿','JJing_e','메구밍','시리우스','Pr','topic','피죤']
class Bot():
    irc = None
    msgQueue = Queue()
    channel_list = []
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
        
    def run(self):
        print('RUNNING')
        while True:
            packet = self.msgQueue.get()
            if packet['type'] == 'msg':
                msg = packet['content']
                for channel in self.channel_list:
                    self.irc.sendmsg(channel, msg)

            elif packet['type'] == 'irc':
                message = packet['content']
                #print(message)
                if message.msgType == 'INVITE':
                    print("%s invites to %s" % (message.sender, message.channel))
                    self.irc.joinchan(message.channel)

                elif message.msgType == 'NOTICE':
                    if message.sender == masterNick and message.channel == botnick:
                        self.irc.semdmsg('#snucse16',message.msg)
                        continue
                elif message.msgType == 'MODE':
                    if message.msg == '+o ' + botnick:
                        self.irc.sendmsg(message.channel, '>ㅅ<')
                    elif message.msg == '-o ' + botnick:
                        self.irc.sendmsg(message.channel, 'ㅇㅅㅇ..')

                elif message.msgType == 'PRIVMSG':
                    if (message.sender in botNameList):
                        continue
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
                            smsg = CFUserInfo(contents)
                            self.irc.sendmsg(message.channel, smsg)
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
                                self.irc.sendmsg(message.channel, 'gs12117에게는 0.3마리의 치킨이면 충분합니다')
                            if EE(num):
                                self.irc.sendmsg(message.channel, '%d명에게는 %d마리의 치킨이 적절합니다' % (num, Chib(int(num))))
                            if Bi(num):
                                self.irc.sendmsg(message.channel, '%s명에게는 %s마리의 치킨이 적절합니다' % (Mkbi(Mkd(num)), Mkbi(Chib(int(Mkd(num))))))
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
                            self.irc.sendmsg(message.channel, title + ' - ' + 'https://boj.kr/%d' % num)
                        elif title == None:
                            self.irc.sendmsg(message.channel, 'Not found')
                        elif title == False:
                            self.irc.sendmsg(message.channel, 'Timeout')
                        continue
                    
                    if message.msg == '!환율':
                        self.irc.sendmsg(message.channel, 'ex)!환율 [숫자] <통화명> [-> <통화명>]')
                        continue
                    
                    if message.msg == '!코포':
                        contestlist = CFContestList()
                        if contestlist != False:
                            if len(contestlist) == 0:
                                self.irc.sendmsg(message.channel, 'No contest yet')
                                continue
                            contestlist = sorted(contestlist, key=lambda con: con[5])
                            for i  in range(min(len(contestlist),2 if message.channel != '#Jhuni' else len(contestlist))):
                                con = contestlist[i]
                                self.irc.sendmsg(message.channel, '[%s] %s | %s | %s | %s' % (con[0],con[1], con[2],con[3],con[4]))
                            continue
                        else:
                            self.irc.sendmsg(message.channel, 'Timeout')
                            continue
                        
                        
                    if message.msg == '부스터 옵줘':
                        self.irc.sendmode(message.channel,'+o ' + message.sender)
                        continue
                    
                    isCalled = False
                    for x in callNameList:
                        if message.msg.find(x) != -1:
                            isCalled = True
                            break
                    if isCalled:
                        continue
                    
                    if message.msg.find('치킨') != -1 and message.msg.find('치킨') < message.msg.find('먹') < message.msg.find('싶'):
                        self.irc.sendmsg(message.channel, '치킨!')
                        continue
                    
                    parse = re.search(r'부(우*)스터(어*)', message.msg)
                    if parse:
                        cry1 = len(parse.group(1))
                        cry2 = len(parse.group(2))
                        self.irc.sendmsg(message.channel, '크' + ('으'*cry1 if cry1 < 10 else '으*%d' % cry1) + ('아'*cry2 if cry2 < 10 else '아*%d' % cry2) + '앙')
                        continue
                    

    def loopExCrawl(self):
        while True:
            time.sleep(30*60)
            self.exList = ExchangeCrawl()
            self.nameDic = MakeNameDic(self.exList)
            self.exDic = UpdateExDic(self.exList, self.exDic)
            
    def loopCFCrawl(self):
        RCList = InitCFChangeList('PJH0123')
        while True:
            time.sleep(10*60)
            newList = CFRatingChange('PJH0123',RCList)
            if newList:
                for i in range(max(len(newList)-2,0),len(newList)):
                    ch = newList[i]
                    RCList.append(ch['contestId'])
                    score = ch['newRating']-ch['oldRating']
                    score = chr(3) + ('12+' if score >= 0 else '07-') + str(abs(score)) + chr(3)
                    self.irc.sendmsg('#Jhuni', "[codeforeces] %s %d -> %d (%s) #%d at contest%d" % ('PJH0123', ch['oldRating'], ch['newRating'], score, ch['rank'], ch['contestId']))

    def start(self):
        threading.Thread(target = self.loopExCrawl, daemon = True).start()
        threading.Thread(target = self.loopCFCrawl, daemon = True).start()
        self.run()
        
if __name__ == '__main__':
    bot = Bot()
    bot.start()
