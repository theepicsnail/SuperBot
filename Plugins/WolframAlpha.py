"""
Google plugin for Superbot.
This plugin handles functionality pertaining to google such as
google search, and google weather.
"""

import urllib2, urllib
import simplejson
import lxml.html
from xml.dom import minidom


HEADERS  = {'User-Agent': "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.5)"}

def getAnswer(question):
    url = "http://www.wolframalpha.com/input/?i="+urllib.quote_plus(question)
    request = urllib2.Request(url, None, HEADERS)
    response = urllib2.urlopen(request)
    data = response.read()
    try:
        res = eval(data.split("context.jsonArray.popups.i_0200_1 =")[1].split(";")[0])
        return res["stringified"]
    except:
        return "Something broke!"

def on_PRIVMSG(bot, sender, args): 
    PREFIX = '!'
    nick, channel, args = sender.split('!', 1)[0], args[0], args[1]
    
    if args.startswith(PREFIX):
        try:
            cmd, msg = args.split(' ', 1)
            if cmd in ["!wa"]:
                bot.say(channel, getAnswer(msg))
        except ValueError:
            cmd, msg = "", ""
            

