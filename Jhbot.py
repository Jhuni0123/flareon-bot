# -*- coding: utf-8 -*-

from ircmessage import IRCMessage
from setting import botnick
from queue import Queue
from score import Sent, Score
from chib import fib, Chib, EE, Bi, Mkbi, Mkd
import re, threading, time
from bojcrawl import BOJCrawl
from cfcrawl import CFCrawl
from exchangecrawl import ExchangeCrawl, MakeNameDic, MakeExDic
class Bot():
    irc = None
    msgQueue = Queue()
    channel_list = []
    exList = None
    nameDic = None
    exDic = None
    nameList = None
    def __init__(self):
        from ircconnector import IRCConnector
        self.irc = IRCConnector(self.msgQueue)
        self.irc.setDaemon(True)
        self.irc.start()
        self.exList = ExchangeCrawl()
        self.nameDic = MakeNameDic(self.exList)
        self.nameList = list(self.nameDic.keys())
        self.exDic = MakeExDic(self.exList)
        
    def run(self):
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
                    if (message.sender in [r'\b','C','bryan_a','cubeIover','VBChunguk_bot','gn','kcm1700-bot','치즈','Diet-bot','JW270','Bonobot']):
                        continue
                    parse = re.match(r'!(\S+)(\s+.*)$',message.msg)
                    if parse:
                        command = parse.group(1)
                        contents = parse.group(2).strip(' \t\n\r')
                        if command == '환율':
                            parse = re.match(r'(\S+)\s*([^0-9 \t\n\r\f\v]*)\s*(\d*)$',contents)
                            if parse:
                                cname = parse.group(1)
                                if parse.group(2) == '공화국':
                                    cname = cname + ' ' + parse.group(2)
                                else:
                                    cname = cname + parse.group(2)
                                num = parse.group(3)
                                if num =='':
                                    num == None
                                else:
                                    num = int(num)
                                if cname == 'info' or cname == '정보':
                                    self.irc.sendmsg(message.channel, self.exList[0][1])
                                    continue
                                if cname == 'help' or cname == '도움':
                                    self.irc.sendmsg(message.channel, 'ex)!환율 (나라|심볼) [(-> (나라|심볼))|정수]')
                                    continue
                                
                                if cname in self.nameList:
                                    cname = self.nameDic[cname]
                                    cname
                                    if self.exDic[cname][1]:
                                        m1 = 100
                                    else:
                                        m1 = 1
                                    m = self.exDic[cname][0]
                                    if num:
                                        m = m/m1
                                        m1 = num
                                        m = m*num
                                    self.irc.sendmsg(message.channel, '%d %s = %.2f KRW' % (m1,cname,m))
                                    continue
                                
                            parse = re.match(r'(\S+)\s*->\s*(\S+)$',contents)
                            if parse:
                                name1 = parse.group(1)
                                name2 = parse.group(2)
                                print(name1,name2)
                                if (name1 in self.nameList) and (name2 in self.nameList):
                                    name1=self.nameDic[name1]
                                    name2=self.nameDic[name2]
                                    m1=self.exDic[name1][0]
                                    m2=self.exDic[name2][0]
                                    
                                    if self.exDic[name1][1]:
                                        m1 = m1/100.0
                                    if self.exDic[name2][1]:
                                        m2 = m2/100.0
                                    print(m1,m2)
                                    self.irc.sendmsg(message.channel, '1 %s = %.4f %s' % (name1, m1/m2, name2))
                                    continue
                                else :
                                    self.irc.sendmsg(message.channel, 'Not found')
                                    continue
                            self.irc.sendmsg(message.channel, 'ex)!환율 (나라|심볼) [-> (나라|심볼)]')
                            continue
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
                    if message.msg == '!코포':
                        contestlist = CFCrawl()
                        if contestlist:
                            for con in contestlist:
                                self.irc.sendmsg(message.channel, '[%s]%s/%s/%s' % (con[0],con[1],con[2],con[3]))
                            continue
                        else:
                            self.irc.sendmsg(message.channel, 'Timeout')
                            continue
                    if message.msg == '부스터 옵줘':
                        self.irc.sendmode(message.channel,'+o ' + message.sender)
                        continue
                    if message.msg.find('부스터') != -1:
                        self.irc.sendmsg(message.channel, '크앙')
                        continue
                    if message.msg.find('치킨') != -1 and message.msg.find('치킨') < message.msg.find('먹') < message.msg.find('싶'):
                        self.irc.sendmsg(message.channel, '치킨!')
                        continue
    def loopCrawl(self):
        while True:
            time.sleep(60*60)
            self.exList = ExchangeCrawl()
            self.nameDic = MakeNameDic(self.exList)
            self.nameList = list(self.nameDic.keys())
            self.exDic = MakeExDic(self.exList)
            
    def start(self):
        threading.Thread(target = self.run,daemon = True).start()
        threading.Thread(target = self.loopCrawl, daemon = True).start()
if __name__ == '__main__':
    bot = Bot()
    bot.start()
