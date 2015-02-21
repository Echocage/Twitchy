global config

config = {  # details required to login to twitch IRC server
            'server': 'irc.twitch.tv',
            'port': 6667,
            'username': 'twitch_username',
            'oauth_password': 'oauth:',  # get this from http://twitchapps.com/tmi/  # channel to join
            'channels': ['#channel_one', '#channel_two'],  # if set to true will display any data received
            'debug': False,
            'log_messages': True,  # maximum amount of bytes to receive from socket - 1024-4096 recommended
            'socket_buffer_size': 2048
}
