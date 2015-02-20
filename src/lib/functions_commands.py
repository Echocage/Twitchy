import time
import importlib

from .command_headers import *


def is_valid_command(command):
    if command in commands:
        return True


def update_last_used(command, channel):
    commands[command][channel]['last_used'] = time.time()


def get_command_limit(command):
    return commands[command]['limit']


def is_on_cooldown(command, channel):
    return time.time() - commands[command][channel]['last_used'] < commands[command]['limit']


def get_cooldown_remaining(command, channel):
    return round(commands[command]['limit'] - (time.time() - commands[command][channel]['last_used']))


def check_has_return(command):
    return  commands[command]['return'] and commands[command]['return'] != 'command'



def get_return(command):
    return commands[command]['return']


def check_has_args(command):
    if 'argc' in commands[command]:
        return True


def check_has_correct_args(message, command):
    message = message.split(' ')
    if len(message) - 1 == commands[command]['argc']:
        return True


def check_returns_function(command):
    if commands[command]['return'] == 'command':
        return True


def pass_to_function(command, args):
    command = command.replace('!', '')

    module = importlib.import_module('src.lib.commands.%s' % command)
    function = getattr(module, command)

    if args:
        return function(args)
    return function()