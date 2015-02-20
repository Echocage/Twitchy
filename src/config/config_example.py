global config

config = {  # details required to login to twitch IRC server
            'server': 'irc.twitch.tv',
            'port': 6667,
            'username': 'echocage',
            'oauth_password': 'oauth:80psxz72qo4crs7ilxqm3yrhl46h2a',  # get this from http://twitchapps.com/tmi/  # channel to join
            'channels': ['#J3wsOfHazard'],  # if set to true will display any data received
            'debug': False,


            'cron': {
                '#channel_one': {
                    'run_cron': False,
                    # set this to false if you want don't want to run the cronjob but you want to preserve the messages etc
                    'run_time': 5,  # time in seconds
                    'cron_messages': [
                        'This is channel_one cron message one.',
                        'This is channel_one cron message two.'
                    ]
                },

                '#channel_two': {
                    'run_cron': False,
                    'run_time': 20,
                    'cron_messages': [
                        'This is channel_two cron message one.'
                    ]
                }
            },  # if set to true will display any data received
            'debug': False,  # if set to true will log all messages from all channels  # todo
            'log_messages': True,  # maximum amount of bytes to receive from socket - 1024-4096 recommended
            'socket_buffer_size': 2048
}

