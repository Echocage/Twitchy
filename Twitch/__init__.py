import logging
import socket
import sys

from Twitch.utils import channels_to_string, check_for_message, get_message, check_login_status


class Twitch:
    def __init__(self, username, oauth, server, port, channels, socket_buffer=2048):
        self.username = username
        self.oauth = oauth
        self.server = server
        self.port = port
        self.channels = channels
        self.socket_buffer = socket_buffer

        self.create_initial_connection()

    def check_for_ping(self, data):
        if data[:4] == "PING":
            self.sock.send('PONG')

    def send_message(self, channel, message):
        self.sock.send(bytes('PRIVMSG %s :%s\n' % (channel, message), 'utf-8'))

    def create_initial_connection(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(10)

        try:
            self.sock.connect((self.server, self.port))
        except:
            logging.error('Cannot connect to server (%s:%s).' % (self.server, self.port))
            sys.exit()

        self.sock.settimeout(None)

        logged_in = self.login()
        if logged_in:
            logging.info('Login successful.')
        else:
            logging.error('Login unsuccessful.'
                          ' (hint: make sure your oauth token is set in self.config/self.config.py).')
            sys.exit()

        self.join_channels(channels_to_string(self.channels))

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
        self.sock.send(bytes('USER %s\r\n' % self.username, 'utf8'))
        self.sock.send(bytes('PASS %s\r\n' % self.oauth, 'utf8'))
        self.sock.send(bytes('NICK %s\r\n' % self.username, 'utf8'))
        return self.is_logged_in()

    def join_channels(self, channels):
        self.sock.send(bytes('JOIN %s\r\n' % channels, encoding='utf8'))

    def leave_channels(self, channels):
        self.sock.send(bytes('PART %s\r\n' % channels, encoding='utf8'))

    @staticmethod
    def from_config(config):
        return Twitch(config['username'], config['oauth_password'], config['server'],
                      config['port'], config['channels'], config['socket_buffer_size'])