import re

class IRCMessage(dict):
    def __init__(self, msg):
        msg = msg.strip()
        self['command'] = None
        self['sender'] = None
        match = re.search('^(?::(\S+) )?([a-zA-Z]+|\d\d\d)((?: [^ :\r\n\0][^ \r\n\0]*)*)(?: :(.*))?$', msg)
        if match:
            sender, command, params, text = match.groups()
            params = params.split()
            self['sender'] = sender
            if sender:
                match = re.search('^([^!@]+)(?:(?:!(\S+))?(@\S+))?$', sender)
                if match:
                    self['sender'] = match.group(1)
                    if match.group(3):
                        self['sender-user'] = (match.group(2) if match.group(2) else match.group(1)) + match.group(3)
            self['command'] = command
            if command == 'PING':
                self['server'] = text.strip()
            elif command in ['NOTICE', 'PRIVMSG', 'TOPIC']:
                self['target'] = params[0]
                self['text'] = text
            elif command == 'INVITE':
                self['target'] = params[1]
            elif command == 'MODE':
                self['target'] = params[0]
                self['mode'] = params[1]
                if len(params) > 2:
                    self['users'] = params[2:]
            elif command == 'ERROR':
                self['text'] = text
            elif command == 'NICK':
                self['nick'] = text
            elif command == '353':
                self['target'] = params[0]
                self['channel_option'] = params[1]
                self['channel'] = params[2]
                self['users'] = text.split()
            elif command == '366':
                self['target'] = params[0]
                self['channel'] = params[1]
                self['text'] = text
            elif command.isnumeric():
                self['target'] = params[0]
                params = params[1:]
                if text != None:
                    params.append(text)
                self['text'] = ' '.join(params)
        else:
            self['text'] = msg
        print(msg)
        print(self)

