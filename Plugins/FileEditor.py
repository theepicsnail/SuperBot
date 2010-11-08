openFiles= {}
def openFile(nick , filename):
    if filename in openFiles.values():
        return -1 # file already open


def readLines(filename, start, end):
    return file(filename).readlines()[start:end]
def deleteLine(filename, lineno):
    f = file(filename)
    lines = f.readlines()
    lines = lines[:lineno]+lines[lineno+1:]
    
def usage(bot,channel):
    pass
def list(bot,channel):
    pass

def on_PRIVMSG(bot, sender, args):
    nick, channel, msg = sender.split('!', 1)[0], args[0], args[1]
    if args[0] == "superbot":
        channel=nick
    if(msg[0:3]==""):
        parts=msg.split(" ")
        print nick,channel,msg,args

        #end of 1-length possibilities 
        if len(args) < 2:
            usage(bot,channel)
            return

        
        if args[1]=="list":
            list(bot,channel)
            return 

        #end of 2-length possibilities
        if len(args)<3:
            usage(bot,channel)
            return                    

        if args[1]=="    
        bot.msg(channel,str(parts))



