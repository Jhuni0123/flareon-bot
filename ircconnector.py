import socket, ssl
import threading
from queue import Queue
from ircmessage import IRCMessage

class IRCConnector:
    def __init__(self, server, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((server, port))
        self._sock = ssl.wrap_socket(s)

        self._msg_queue = Queue()
        _thread = threading.Thread(target = self.recv_msg, daemon = True)
        _thread.start()

    def init_user(self, name):
        self._send('USER ' + (name + ' ') * 3 + ':' + name)

    def set_nick(self, nick):
        self._send('NICK ' + nick)

    def join_chan(self, chan_name):
        self._send('JOIN ' + chan_name)

    def get_names(self, chan_name):
        self._send('NAMES ' + chan_name)

    def send_msg(self, target, text):
        self._send('PRIVMSG ' + target + ' :' + text)

    def set_topic(self, chan_name, text):
        self._send('TOPIC ' + chan_name + ' :' + text)

    def part_chan(self, chan_name, text = ''):
        self._send('PART ' + chan_name + ' ' + text)

    def quit(self, text):
        self._send('QUIT ' + text)

    def pong(self, server):
        self._send('PONG ' + server)

    def _send(self, text):
        self._sock.send((text + '\n').encode())

    def get_next_msg(self):
        return self._msg_queue.get()

    def recv_msg(self):
        prefix = b''
        while True:
            raw_bytes = self._sock.recv(1024)
            if raw_bytes:
                raw_bytes = prefix + raw_bytes
                msg_list = raw_bytes.split(b'\r\n')
                prefix = msg_list[-1]
                msg_list.pop()
                for msg_bytes in msg_list:
                    msg_str = msg_bytes.decode(errors = 'ignore')
                    msg = IRCMessage(msg_str)
                    if msg['command'] == 'PING':
                        self.pong(msg['server'])
                    else:
                        self._msg_queue.put(msg)
            else:
                self._sock.close()
                print('Connection closed')
                break
