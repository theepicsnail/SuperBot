def on_load(bot):
    bot.say("#adullam","error tests loaded")
    
def on_PRIVMSG(bot,sender,args):
#   print "XX:",bot,sender,args
#    bot.say("#adullam","privmsg")
    if "fake" in args:
        nonExistantFunctionCall()
    elif "rec" in args:
        rec()
def rec():
    rec()


