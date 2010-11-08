#def on_load(bot):
#def on_unload(bot):
#
# 
#   Username    Password?   Credits     I don't know what else 
def on_PRIVMSG(bot,sender,msg):
    respondTo = sender.split("!")[0] if msg[0] == bot.nickname else msg[0]
    print "respondTo",respondTo    
