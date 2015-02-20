import logging
import socket
import re
import sys


class Twitch:
    def __init__(self, config):
        self.config = config
        self.create_initial_connection()

    def check_for_ping(self, data):
        if data[:4] == "PING":
            self.sock.send('PONG')

    def send_message(self, channel, message):
        self.sock.send('PRIVMSG %s :%s\n' % (channel, message.encode('utf-8')))

    def create_initial_connection(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(10)

        try:
            self.sock.connect((self.config['server'], self.config['port']))
        except:
            logging.error('Cannot connect to server (%s:%s).' % (self.config['server'], self.config['port']))
            sys.exit()

        self.sock.settimeout(None)

        logged_in = self.login()
        if logged_in:
            logging.info('Login successful.')
        else:
            logging.error('Login unsuccessful.'
                          ' (hint: make sure your oauth token is set in self.config/self.config.py).')
            sys.exit()

        self.join_channels(channels_to_string(self.config['channels']))

    def _get_update(self):
        data = self.sock.recv(self.config['socket_buffer_size']).rstrip()
        if len(data) == 0:
            logging.warning('Connection was lost, reconnecting.')
            self.socket = self.irc.create_initial_connection()
            return
        self.check_for_ping(data)

        if not check_for_message(data):
            return
        return get_message(data)

    def get_messages(self):
        while True:
            data = self._get_update()
            if not data:
                continue
            yield data


    def is_logged_in(self):
        return check_login_status(self.sock.recv(1024))

    def login(self):
        self.sock.send(bytes('USER %s\r\n' % self.config['username'], 'utf8'))
        self.sock.send(bytes('PASS %s\r\n' % self.config['oauth_password'], 'utf8'))
        self.sock.send(bytes('NICK %s\r\n' % self.config['username'], 'utf8'))
        return self.is_logged_in()

    def join_channels(self, channels):
        self.sock.send(bytes('JOIN %s\r\n' % channels, encoding='utf8'))

    def leave_channels(self, channels):
        self.sock.send(bytes('PART %s\r\n' % channels, encoding='utf8'))


def check_for_message(data):
    return bool(re.match(r'^:[a-zA-Z0-9_]+\![a-zA-Z0-9_]+@[a-zA-Z0-9_]+(\.tmi\.twitch\.tv|\.testserver\.local) '
                         r'PRIVMSG #[a-zA-Z0-9_]+ :.+$', data.decode('utf8')))


def check_is_command(message, valid_commands):
    for command in valid_commands:
        if command == message:
            return True


def check_for_connected(data):
    return bool(re.match(r'^:.+ 001 .+ :connected to TMI$', data))


def get_message(data):
    channel = re.findall(r'^:.+\![a-zA-Z0-9_]+@[a-zA-Z0-9_]+.+ PRIVMSG (.*?) :', data.decode('utf8'))[0]
    username = re.findall(r'^:([a-zA-Z0-9_]+)\!', data.decode('utf8'))[0]
    message = re.findall(r'PRIVMSG #[a-zA-Z0-9_]+ :(.+)', data.decode('utf8'))[0]
    return channel, username, message


def check_login_status(data):
    matches = re.match(r'^:(testserver\.local|tmi\.twitch\.tv) NOTICE \* :Login unsuccessful\r\n$',
                       data.decode('utf-8'))
    return not bool(matches)


def channels_to_string(channel_list):
    return ','.join(channel_list)