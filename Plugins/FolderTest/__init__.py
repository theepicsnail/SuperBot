
def on_PRIVMSG(bot,nick,msg):
    source = msg[0]
    if source == bot.nickname:
        source = nick.split("!")[0]
    msg = msg[1]
    if msg.startswith("!"):
        bot.msg(source,"This test worked!")

    
