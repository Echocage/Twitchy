#!/usr/bin/env python
import logging

from src.bot import *
from src.config.config_example import config
logging.basicConfig(level=logging.DEBUG)

bot = Roboraj(config).run()
