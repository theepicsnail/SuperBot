"""
Games plugin for Superbot.
Various games to be used within an IRC channel. 
This code is borrowed from around the web.

So i think that implementing something where you have fake money 'credits'
and they spend the credits to play black jack or something 
also if you run out you can always reset your account so you get say 400 credits

"""
import random

def coin():
    if random.randrange(0, 2):
        return "You flipped: Heads"
    else:
        return "You flipped: Tails"

def dice():
    pass



def on_PRIVMSG(bot, sender, args):
    PREFIX = '!'
    nick, channel, args = sender.split('!', 1)[0], args[0], args[1]
    
    if args.startswith(PREFIX):
        try: 
            cmd, msg = args.split(' ', 1)  
        except ValueError:
            cmd, msg = args, ""
        if cmd == '!coin':
            bot.say(channel, coin())



