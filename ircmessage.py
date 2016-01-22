import re


class IRCMessage():
    msgType = None
    sender = None
    channel = None
    msg = None
    target = None

    def __init__(self, origMessage):
        parse = re.search('^(?:[:](\S+)!\S+ )?(\S+)(?: (?!:)(.+?))?(?: [:](.+))?$', origMessage)
        if parse:
            self.msgType = parse.group(2)
            if self.msgType == 'INVITE':
                self.sender = parse.group(1)
                self.target = parse.group(3)
                self.channel = parse.group(4)
            if self.msgType == 'NOTICE':
                self.sender = parse.group(1)
                self.channel = parse.group(3)
                self.msg = parse.group(4)
            elif self.msgType == 'PRIVMSG':
                self.sender = parse.group(1)
                self.channel = parse.group(3)
                self.msg = parse.group(4)
                if self.sender == 'B':
                    parse = re.match('<.(\S+)> (.*)$', self.msg)
                    if parse:
                        self.sender = parse.group(1)
                        self.msg = parse.group(2)
            elif self.msgType == 'MODE':
                self.sender = parse.group(1)
                self.channel = parse.group(3).split(' ', maxsplit=1)[0]
                self.msg = parse.group(3).split(' ', maxsplit=1)[1]
            elif self.msgType == 'JOIN':
                self.sender = parse.group(1)
                self.channel = parse.group(4)
            elif self.msgType == 'PING':
                self.sender = parse.group(4)
        else:
            pass

    def __repr__(self):
        msg = self.msg
        return '<IRCMessage : %s %s %s %s %s>' \
               % (self.msgType, self.sender, self.channel, msg, self.target)

    def isValid(self):
        if self.msgType == None:
            return False
        else:
            return True
