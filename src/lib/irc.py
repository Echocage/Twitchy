import logging
import socket
import re
import sys
from threading import Thread

from . import cron


def check_for_message(data):
    return bool(re.match(r'^:[a-zA-Z0-9_]+\![a-zA-Z0-9_]+@[a-zA-Z0-9_]+(\.tmi\.twitch\.tv|\.testserver\.local) '
                         r'PRIVMSG #[a-zA-Z0-9_]+ :.+$', data))


def check_is_command(message, valid_commands):
    for command in valid_commands:
        if command == message:
            return True


def check_for_connected(data):
    return bool(re.match(r'^:.+ 001 .+ :connected to TMI$', data))


def get_message(data):
    return {
        'channel': re.findall(r'^:.+\![a-zA-Z0-9_]+@[a-zA-Z0-9_]+.+ PRIVMSG (.*?) :', data)[0],
        'username': re.findall(r'^:([a-zA-Z0-9_]+)\!', data)[0],
        'message': re.findall(r'PRIVMSG #[a-zA-Z0-9_]+ :(.+)', data)[0].decode('utf8')
    }


def check_login_status(data):
    matches = re.match(r'^:(testserver\.local|tmi\.twitch\.tv) NOTICE \* :Login unsuccessful\r\n$',
                       data.decode('utf-8'))
    return not bool(matches)


def channels_to_string(channel_list):
    return ','.join(channel_list)


class irc:
    def __init__(self, config):
        self.config = config

    def check_for_ping(self, data):
        if data[:4] == "PING":
            self.sock.send('PONG')

    def send_message(self, channel, message):
        self.sock.send('PRIVMSG %s :%s\n' % (channel, message.encode('utf-8')))

    def get_irc_socket_object(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)

        self.sock = sock

        try:
            sock.connect((self.config['server'], self.config['port']))
        except:
            logging.error('Cannot connect to server (%s:%s).' % (self.config['server'], self.config['port']))
            sys.exit()

        sock.settimeout(None)

        sock.send(bytes('USER %s\r\n' % self.config['username'], 'utf8'))
        sock.send(bytes('PASS %s\r\n' % self.config['oauth_password'], 'utf8'))
        sock.send(bytes('NICK %s\r\n' % self.config['username'], 'utf8'))

        if check_login_status(sock.recv(1024)):
            logging.info('Login successful.')
        else:
            logging.error('Login unsuccessful.'
                          ' (hint: make sure your oauth token is set in self.config/self.config.py).')
            sys.exit()

        # start threads for channels that have cron messages to run
        for channel in self.config['channels']:
            if channel in self.config['cron']:
                if self.config['cron'][channel]['run_cron']:
                    Thread(target=cron.cron(self, channel).run)

        self.join_channels(channels_to_string(self.config['channels']))

        return sock

    def join_channels(self, channels):
        self.sock.send(bytes('JOIN %s\r\n' % channels, encoding='utf8'))

    def leave_channels(self, channels):
        self.sock.send(bytes('PART %s\r\n' % channels, encoding='utf8'))

