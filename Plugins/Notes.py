NoteDirectory = "notes"

def listDir(bot):
    pass
def newFile(bot,filename, password):
    pass
def deleteFile(



word= "([^\x20]+)"
commands=[
#Possible functions:
#!N list
("!N list",listDir),
#!N new $name
("!N new "+word,newFile),
#!N delete $name [$password]
("!N delete "+word+"(?: "+word+")?" ,deleteFile),
#
#!N open $name [$password]
("!N open "+word+"(?: "+word+")?", openFile),
#!N close $name 
("!N close "+word+"(?: "+word+")?", closeFile),
#
#!N read [line number|'all']
#!N append $line
#!N set $line $data
#
#files will have attributes
#they will be line based
#possibly encrypted (woah) 
#
#File format:
#1st line :
#creator \t creationdate 
#
#
#
#



def usage(bot,channel):
    pass
def list(bot,channel):
    pass

def on_PRIVMSG(bot, sender, args):
    nick, channel, msg = sender.split('!', 1)[0], args[0], args[1]
    if args[0] == "superbot":
        channel=nick
    if(msg[0:3]=="!N "):
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



