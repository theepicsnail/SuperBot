
def on_load(b):
    pass
def on_unload(bot):
    pass

MSGSIZE=500
def on_PRIVMSG(bot, sender, args):
    nick, channel, msg = sender.split('!', 1)[0], args[0], args[1]
    if channel!=bot.nickname:
        return #this plugin should only be done in PMs
    if msg.startswith(">"):
        msg = msg[1:]
        showAll = False
        if msg.startswith(">"):
            showAll=True
            msg = msg[1:]
        try:
            if nick in ["snail","broken"]: # i don't think anyone else would really work on superbot
                out = str(eval(msg))
        except Exception as E:
            out = "ERROR: "+str(E)
        if len(out)>MSGSIZE:
            if showAll:
                while len(out)!=0:
                    bot.msg(nick,out[:MSGSIZE])
                    out = out[MSGSIZE:]
            else:
                bot.msg(nick,"Message truncated, use >> instead of > to see full output (full output is "+str(len(out)/MSGSIZE+1)+" messages)")
                bot.msg(nick,out[:MSGSIZE])
        else:
            bot.msg(nick,out)
    pass




