import shelve
from datetime import datetime,timedelta
db = None

prefix="$"
channel="#test"

def on_load(b):
    global db
    db = shelve.open("m528.db", writeback=True) #if this causes problems it's not necessary 
    pass

def on_unload(bot):
    db.close()
    pass

def on_NOTICE(bot, sender, args):
    updateTopic(bot)
def updateTopic(bot):
    title=""
    color = 2
    for user in db.keys():
        privdb = db[user]
        color = color +1 
        if color == 15:
            color = 3
        title+=chr(3)+str(color)+"|"+user+" "
        for event in privdb.keys():
            time= str((datetime.now()-privdb[event]).days)
            title+=event+":"+time+" "
#        title+="]"
    print title
    bot.topic(channel,title)

def on_PRIVMSG(bot, sender, args):
    nick, chan, msg = sender.split('!', 1)[0], args[0], args[1]
    
    update= False
    if chan==channel and msg.startswith(prefix):
        args = msg.split(None,1)

        privdb={}
        if db.has_key(nick):
            privdb=db[nick]

        key = args[0][1:]
        length = None
        if privdb.has_key(key):
            length = (datetime.now()-privdb[key]).days
            if length!=1:
                length = str(length)+" days"
            else:
                length = str(length)+" day"
                

        if len(args)==1:
            if length:
                bot.say(channel,"Timer reset, length = "+length)
            else:
                bot.say(channel,"New timer started! Be strong!")

            privdb[key]=datetime.now()
            update = True
        else:
            if args[1]=="remove":
                if length:
                    bot.say(channel,"Timer removed.  length = "+length)
                    del privdb[key]
                    update = True
                else:
                    bot.say(channel,"You never had that timer!")

            elif args[1]=="stat":
                if length:
                    bot.say(channel,length)
                else:
                    bot.say(channel,"You never started that timer, use "+prefix+key+" to start it!")
            else:
                try:
                    d = int(args[1])
                    length = str(d)+" day"
                    if d!=1:
                        length += "s"
                    td = timedelta(days=d)
                    privdb[key]=datetime.now()-td
                    bot.say(channel,"Timer reset, length = "+length)
                    update = True
                except:
                    bot.say(channel,"Try: "+prefix+key+" # to set the number of days on your timer")

        db[nick]=privdb

        if update:
            updateTopic(bot)
    pass


