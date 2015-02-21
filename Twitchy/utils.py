import re


CONTAINS_MESSAGE = r'^:[a-zA-Z0-9_]+\![a-zA-Z0-9_]+@[a-zA-Z0-9_]+(\.tmi\.twitch\.tv|\.testserver\.local) ' \
                   r'PRIVMSG #[a-zA-Z0-9_]+ :.+$'
CONNECTED_REGEX = r'^:.+ 001 .+ :connected to TMI$'
CHANNEL_REGEX = r'^:.+\![a-zA-Z0-9_]+@[a-zA-Z0-9_]+.+ PRIVMSG (.*?) :'
USERNAME_REGEX = r'^:([a-zA-Z0-9_]+)\!'
MESSAGE_REGEX = r'PRIVMSG #[a-zA-Z0-9_]+ :(.+)'
LOGIN_REGEX = r'^:(testserver\.local|tmi\.twitch\.tv) NOTICE \* :Login unsuccessful\r\n$'


def _decode(data):
    if type(data) is bytes:
        return data.decode('utf8')
    return data


def check_for_message(data):
    return bool(re.match(CONTAINS_MESSAGE, _decode(data)))


def check_is_command(message, valid_commands):
    for command in valid_commands:
        if command == message:
            return True


def check_for_connected(data):
    return bool(re.match(CONNECTED_REGEX, _decode(data)))


def get_message(data):
    channel = re.findall(CHANNEL_REGEX, _decode(data))[0]
    username = re.findall(USERNAME_REGEX, _decode(data))[0]
    message = re.findall(MESSAGE_REGEX, _decode(data))[0]
    return channel, username, message


def check_login_status(data):
    return not bool(re.match(LOGIN_REGEX, _decode(data)))


def channels_to_string(channel_list):
    return ','.join(channel_list)