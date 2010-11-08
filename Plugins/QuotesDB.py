"""
Random quote from the quotes.db
"""

import sqlite3
from random import randint
import re
def randomAwesomeFuckingQuoteYEAH(q=None):
    conn = sqlite3.connect('quotes.db')
    c = conn.cursor()#why >= and not just == i copied this from some mailing list i didn't realy read it lol
    if q:
        c.execute("select * from quotes where quote like ? ORDER BY RANDOM () LIMIT 1;",("%"+q+"%",)) 
        
    else:
        c.execute('''SELECT * FROM quotes ORDER BY RANDOM () LIMIT 1;''')
    tmp = c.fetchall()
    print len(tmp) #this printed out 0 
    quote = list(tmp[0])
    if q:
        i = re.compile("("+q+")", re.IGNORECASE)
        quote[3] = i.sub("{B}\\1{}",quote[3])
    print quote
    c.close()
    conn.close()
    return "<{B}Quote{}: %s --%s on %s [%s]>" % (quote[3].strip(), quote[2].strip(), quote[1].strip(), quote[0])

def on_PRIVMSG(bot, sender, args):
    PREFIX = '!'
    nick, channel, args = sender.split('!', 1)[0], args[0], args[1]
    
    if args.startswith(PREFIX):
        try: 
            cmd, msg = args.split(' ', 1)  
        except ValueError:
            cmd, msg = args, ""
        if cmd in ['!qt', '!quote']:
            bot.say(channel, randomAwesomeFuckingQuoteYEAH(q=msg))


