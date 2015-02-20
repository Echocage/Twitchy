#!/usr/bin/env python
import logging

from Twitch import Twitch
from Twitch.config import config


logging.basicConfig(level=logging.DEBUG)

irc = Twitch.from_config(config)

for channel, user, message in irc.get_messages():
    if message.startswith('!output'):
        irc.send_message(channel, '{} this is an output message'.format(user))