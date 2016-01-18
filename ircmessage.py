#-*- coding: utf-8 -*-
import re

class IRCMessage():
    msgType = None
    senderNick = None
    sender =None
    channel = None
    msg = None
    target = None

    def __init__(self, origMessage):
        parse = re.search(r'^:(.*)!~?(\S+)\s+(\S+)\s+(.*?)\s+:?(.*)',origMessage)
        if parse:
            self.senderNick = parse.group(1)
            self.sender = parse.group(2)
            self.msgType = parse.group(3)
            self.channel = parse.group(4)
            self.msg = parse.group(5)
            if self.msgType == 'INVITE':
                self.channel = parse.group(5)
            if self.senderNick == 'B':
                parse = re.match(r'<.(\S+)> (.*)',self.msg)
                if parse:
                    self.sendernick = parse.group(1)
                    self.msg = parse.group(2)
            if self.msg:
                self.msg = self.msg.decode('utf-8')
            
        else:
            pass


    def __repr__(self):
        msg = self.msg
        if msg:
            msg = msg.encode('utf-8')
        return '<IRCMessage : %s %s %s %s %s %s>' % (self.msgType, self.senderNick, self.sender, self.channel, msg, self.target)
