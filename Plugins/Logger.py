"""
Logger plugin for Superbot.
Logs messages to a database, differentiates between PRIVMSG and ACTIONS
"""
try:
    from Private import LoggerInfo
except: pass

import MySQLdb
import time
def log2db(nick, message, channel, type):
    """
        Simple log to a mysql DB. 
    """
    print LoggerInfo.host
    
    CONNECTION = MySQLdb.connect(
        host = LoggerInfo.host,
        user = LoggerInfo.user,
        passwd = LoggerInfo.passwd,
        db = LoggerInfo.db
    )
       
    cursor = CONNECTION.cursor() 
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    cursor.execute('''INSERT INTO `logger_log` (nick,created,msg,type,channel) VALUES (%s, %s, %s, %s, %s)''', (nick, timestamp, message, type, channel))
    cursor.close()
    CONNECTION.close()  

def on_PRIVMSG(bot, sender, args):
    if ord(args[1][0])==1: return #action, let on_ACTION handle it
    nick, channel, msg = sender.split('!', 1)[0], args[0], args[1]
    log2db(nick, msg, channel, "msg")

def on_ACTION(bot, sender, args):
    nick, channel, msg = sender.split('!', 1)[0], args[0], args[1]
    log2db(nick, msg, channel, "action")


if __name__=="__main__":
    #DONT COMMIT WITH THIS CODE
    host = "localhost"
    user = "superbot"
    passwd = "sup3rb0t!"
    db = "superbotdb"
    CONNECTION = MySQLdb.connect(
        host = host,
        user = user,
        passwd = passwd,
        db = db
    )
       
    cursor = CONNECTION.cursor() 
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    #cursor.execute('''INSERT INTO `logger_log` (nick,created,msg,type,channel) VALUES (%s, %s, %s, %s, %s)''', (nick, timestamp, message, type, channel))
    cursor.execute('''SELECT * from logger_log ''')
    count = [0]*24*60
    for num,nick,created,msg,typ,channel in cursor:
        count[created.hour*60+created.minute] += 1
    cursor.close()
    CONNECTION.close()  
    for i in count:
        print i
   
