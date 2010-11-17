

def on_load(b):
    pass
def on_unload(bot):
    pass


rep = [ ("<3", "{C4}<3{}") ]


def on_PRIVMSG(bot, sender, args):
    nick, channel, msg = sender.split('!', 1)[0], args[0], args[1]
    
    start = msg
    
    for i in rep:
        msg = msg.replace(*i)
    if msg != start:
        bot.say(channel,msg)
    pass




