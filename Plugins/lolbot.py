
lolCount = 0
def on_PRIVMSG(bot, sender, args):
    global lolCount
    nick, channel, args = sender.split('!', 1)[0], args[0], args[1]
   
    if args=="lol":
        lolCount += 1;
        if lolCount == 2:
            lolCount = 0;
            bot.say(channel,"lol")
    else:
        lolCount=0
