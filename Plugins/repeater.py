
hist = ""
def on_PRIVMSG(bot, sender, args):
    global hist
    nick, channel, args = sender.split('!', 1)[0], args[0], args[1]
    if hist == args:
        bot.say(channel,args)
        hist = ""
    else:
        hist = args 
