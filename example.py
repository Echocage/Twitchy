#!/usr/bin/env python
import logging

from Twitch import Irc
from Twitch.config import config

logging.basicConfig(level=logging.DEBUG)

twitch_chat = Irc.from_config(config)
twitch_chat.login()

for channel, user, message in twitch_chat.get_messages():
    print('{}:{}'.format(user, message))