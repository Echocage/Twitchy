import unittest
from unittest.mock import Mock, patch, call

from Twitch import Irc
import Twitch


class TestTwitchy(unittest.TestCase):
    def setUp(self):
        Irc.create_initial_connection = Mock(type=str)
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

    def test_login(self):
        with patch('Twitch.Irc.is_logged_in', return_value=False) as mock_logged_in:
            self.assertFalse(self.example_twitch.login())
            self.assertEqual(self.example_twitch.sock.send.call_count, 3)

            mock_logged_in.return_value = True
            Irc.join_channels = Mock()
            Twitch.channels_to_string = Mock()
            self.assertTrue(self.example_twitch.login())

    def test_send(self):
        self.example_twitch.send('123')
        self.assertEqual(self.example_twitch.sock.send.call_count, 1)
        self.assertEqual(self.example_twitch.sock.send.call_args, call(b'123'))


if __name__ == '__main__':
    unittest.main()