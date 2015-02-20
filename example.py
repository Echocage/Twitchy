#!/usr/bin/env python
import logging
from Twitch import Twitch
from Twitch.config_example import config
logging.basicConfig(level=logging.DEBUG)

irc = Twitch(config)

for message in irc.get_messages():
    print(message)

