# Twitchy
An intuitive python Twitch IRC api


Example:

    from Twitchy import Irc
    from Twitchy.config import config
    
        
    twitch_chat = Irc.from_config(config)
    twitch_chat.login()
        
    for channel, user, message in twitch_chat.get_messages():
        print('{}:{}'.format(user, message))
