#-*- coding: utf-8 -*-

import sys
import socket, ssl
import re
from setting import server, port, botname, botnick
from ircmessage import IRCMessage
from score import Score, Sent
from chib import Chib,EE,fib,Bi,Mkd, Mkbi
def ping():
    ircsock.send('PONG :pingis\n')


def sendmsg(chan, msg):
    ircsock.send('PRIVMSG ' + chan + ' :' +msg + '\n')


def joinchan(chan):
    ircsock.send('JOIN ' + chan + '\n')


def partchan(chan):
    ircsock.send('PART ' + chan + '\n')


def chanlist():
    ircsock.send('WHOIS ' + botnick + '\n')


def runbot():
    while 1:
        ircmsg = ircsock.recv(8192)
        ircmsg = ircmsg.strip('\n\r')
        if ircmsg.find('PING :') != -1:
           ping()
           continue

        print
        print ircmsg

        if ircmsg[0] != ':':
            continue

        message = IRCMessage(ircmsg)
        print message
        print message.msg


        if message.msgType == 'MODE':
            if re.match('\+o+.*',message.msg) and message.msg.find('Jh-bot'):
                sendmsg(message.channel, '고마워요 %s!' % message.senderNick) 
        if message.msgType == 'PRIVMSG':
            parse = re.match(ur'!(\S+)\s+(.*)',message.msg)
            if parse:
                command = parse.group(1)
                contents = parse.group(2)
                if command == ur'점수' or command == ur'score':
                    sen = Sent(contents)
                    if sen == '':
                        sendmsg(message.channel, "'%s'은(는) 적절하지 않은 영단어입니다" % contents.encode('utf-8'))
                        continue
                    scr = Score(sen)
                    if scr == 100:
                        sendmsg(message.channel, "'%s'은(는) %d점짜리 입니다" % (contents.encode('utf-8'),scr))
                    else:
                        sendmsg(message.channel, "'%s'은(는) %d점" % (contents.encode('utf-8'), scr))
                    continue
                
            parse = re.match(ur'!치킨\s+(\d+)\s*(\S*)',message.msg)
            if parse:
                num = long(parse.group(1))
                ex = parse.group(2)
                if ex == ur'명' or ex == ur'':
                    if num == 1:
                        sendmsg(message.channel, '1인1닭은 진리입니다')
                    elif num == 2:
                        sendmsg(message.channel, '계산상 1마리지만 1인1닭의 진리에 따라 2마리의 치킨이 적절합니다')
                    elif num >= 573147844013817084101:
                        sendmsg(message.channel, '필요한 치킨이 너무 많아 셀 수 없습니다')
                        continue
                    else:
                        sendmsg(message.channel, '%d명에게는 %d마리의 치킨이 적절합니다' % (num, Chib(long(num))))
                    if num == 12117:
                        sendmsg(message.channel, 'gs12117에게는 0.5마리의 치킨이면 충분합니다')
                    if EE(num):
                        sendmsg(message.channel, '%d명에게는 %d마리의 치킨이 적절합니다' % (num, Chib(long(num))))
                    if Bi(num):
                        sendmsg(message.channel, '%s명에게는 %s마리의 치킨이 적절합니다' % (Mkbi(Mkd(num)), Mkbi(Chib(long(Mkd(num))))))
                    continue
            if message.msg.find(ur'치킨') != -1 and message.msg.find(ur'치킨') < message.msg.find(ur'먹') < message.msg.find(ur'싶'):
                sendmsg(message.channel, '치킨은 언제나 당신의 곁에')
                continue
            if re.match(ur'!fib\s+-?\d+$',message.msg):
                num = long(re.match(ur'!fib\s+(-?\d+)$',message.msg).group(1))
                if num > 256:
                    sendmsg(message.channel, '[fib] result is too big')
                elif num < 0:
                    sendmsg(message.channel, '[fib] incorrect input')
                else:
                    sendmsg(message.channel, '[fib] %d' % fib[num])
                continue
        


 
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.connect((server,port))
ircsock = ssl.wrap_socket(soc)
ircsock.send('USER ' + (botname +' ') * 3 + ':' + botnick + '\n')
ircsock.send('NICK ' + botnick + '\n')
joinchan('#snucse16')

if __name__ == '__main__':
    runbot()
