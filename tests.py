import socket
import unittest
from unittest.mock import Mock, patch, call

from Twitchy import Irc
import Twitchy


class TestTwitchy(unittest.TestCase):
    def setUp(self):
        with patch('Twitchy.Irc.create_initial_connection', return_value=Mock()):
            self.example_twitch = Irc('abc', '123', '123', '123', '#blah')

    def test_check_for_ping(self):
        self.example_twitch.check_for_ping('PING ksjadlfjdsakl;fjdksalpf')
        self.assertTrue(self.example_twitch.sock.send.called)
        self.example_twitch.check_for_ping('-PING dsaf')
        self.assertEqual(self.example_twitch.sock.send.call_count, 1)

    def test_send_message(self):
        self.example_twitch.send_message('blah', '')
        self.assertTrue(self.example_twitch.sock.send.called)
        self.assertEqual(self.example_twitch.sock.send.call_args, call(b'PRIVMSG blah :\n'))


    def test_create_initial_connection(self):
        with patch('socket.socket', return_value=Mock()) as mock_socket:
            sock = self.example_twitch.create_initial_connection()
            self.assertEqual(mock_socket.call_args, call(socket.AF_INET, socket.SOCK_STREAM))
        self.assertEqual(sock.connect.call_args, call(('123', '123')))

    @patch('Twitchy.Irc.is_logged_in', return_value=False)
    def test_login(self, mock_logged_in):
        self.assertFalse(self.example_twitch.login())
        self.assertEqual(self.example_twitch.sock.send.call_count, 3)

        mock_logged_in.return_value = True
        Irc.join_channels = Mock()
        Twitchy.channels_to_string = Mock()
        self.assertTrue(self.example_twitch.login())

    def test_send(self):
        self.example_twitch.send('123')
        self.assertEqual(self.example_twitch.sock.send.call_count, 1)
        self.assertEqual(self.example_twitch.sock.send.call_args, call(b'123'))

    @patch('Twitchy.check_login_status')
    def test_is_logged_in(self, mock_check_login):
        self.example_twitch.is_logged_in()
        self.assertTrue(mock_check_login.called)


if __name__ == '__main__':
    unittest.main()