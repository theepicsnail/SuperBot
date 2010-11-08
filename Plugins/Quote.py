"""
Quote plugin for Superbot.
This plugin allows you to quote a users last messages to be saved into a 
quotes database. Only keeps track of 10 messages per nick.
"""

HISTORY = {}

def on_PRIVMSG(bot, sender, args):
    PREFIX = '!'
    nick, channel, args = sender.split('!', 1)[0], args[0], args[1]
   
    if args.startswith(PREFIX):
        try:
            cmd, msg = args.split(' ', 1)
            if cmd == '!quote':
                for part in msg.split(' '):
                    n=part
                    try:
                        n,num = part.split(",",1)
                    except ValueError:
                        num = "1"
                    num = int(num)
                    print "n,num",n,num
                    if HISTORY.has_key(n):
                        try:
                            bot.say(channel, HISTORY[n][-1*num])
                        except:
                            bot.say(channel,"Something broke!")
        except ValueError:
            cmd, msg = "",""

    if not HISTORY.has_key(nick):
        HISTORY[nick] = [""]*10 
    HISTORY[nick] = HISTORY[nick][1:]+[args] 
