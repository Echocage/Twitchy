import re


def check_for_message(data):
    return bool(re.match(r'^:[a-zA-Z0-9_]+\![a-zA-Z0-9_]+@[a-zA-Z0-9_]+(\.tmi\.twitch\.tv|\.testserver\.local) '
                         r'PRIVMSG #[a-zA-Z0-9_]+ :.+$', data.decode('utf8')))


def check_is_command(message, valid_commands):
    for command in valid_commands:
        if command == message:
            return True


def check_for_connected(data):
    return bool(re.match(r'^:.+ 001 .+ :connected to TMI$', data))


def get_message(data):
    channel = re.findall(r'^:.+\![a-zA-Z0-9_]+@[a-zA-Z0-9_]+.+ PRIVMSG (.*?) :', data.decode('utf8'))[0]
    username = re.findall(r'^:([a-zA-Z0-9_]+)\!', data.decode('utf8'))[0]
    message = re.findall(r'PRIVMSG #[a-zA-Z0-9_]+ :(.+)', data.decode('utf8'))[0]
    return channel, username, message


def check_login_status(data):
    matches = re.match(r'^:(testserver\.local|tmi\.twitch\.tv) NOTICE \* :Login unsuccessful\r\n$',
                       data.decode('utf-8'))
    return not bool(matches)


def channels_to_string(channel_list):
    return ','.join(channel_list)