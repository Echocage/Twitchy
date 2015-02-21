import logging
import socket
import sys

from Twitch.utils import channels_to_string, check_for_message, get_message, check_login_status


class Irc:
    def __init__(self, username, oauth, server, port, channels, socket_buffer=2048):
        self.username = username
        self.oauth = oauth
        self.server = server
        self.port = port
        self.channels = channels
        self.socket_buffer = socket_buffer
        self.sock = self.create_initial_connection()

    def check_for_ping(self, data):
        if data[:4] == "PING":
            self.sock.send('PONG')

    def send_message(self, channel, message):
        self.send('PRIVMSG %s :%s\n' % (channel, message))

    def create_initial_connection(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)

        try:
            sock.connect((self.server, self.port))
        except:
            logging.error('Cannot connect to server (%s:%s).' % (self.server, self.port))
            sys.exit()

        sock.settimeout(None)
        return sock

    def _get_update(self):
        data = self.sock.recv(self.socket_buffer).rstrip()
        if len(data) == 0:
            logging.warning('Connection was lost, reconnecting.')
            self.create_initial_connection()
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
        commands = ['USER %s\r\n' % self.username, 'PASS %s\r\n' % self.oauth, 'NICK %s\r\n' % self.username]
        for command in commands:
            self.send(command)

        logged_in = self.is_logged_in()
        if logged_in:
            logging.info('Login successful.')
            self.join_channels(channels_to_string(self.channels))
        else:
            logging.error(
                'Login unsuccessful.(hint: make sure your oauth token is set in self.config/self.config.py).')

        return logged_in

    def send(self, data, encoding='utf-8'):
        if type(data) is str:
            data = bytes(data, encoding)
        self.sock.send(data)

    def join_channels(self, channels):
        self.send('JOIN %s\r\n' % channels)


    def leave_channels(self, channels):
        self.send('PART %s\r\n' % channels)


    @staticmethod
    def from_config(config):
        return Irc(config['username'], config['oauth_password'], config['server'],
                      config['port'], config['channels'], config['socket_buffer_size'])