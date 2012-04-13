"""URL Shortening via the Bitly API for use within IRC"""

import urllib2
import re
import urllib

LOGIN = "tsoporan"
API_KEY = "R_e29b3e8186e3fec26cbb30963dfc3747"
API_URL = "http://api.bit.ly/v3/shorten?login=%s&apiKey=%s&longUrl=%s&format=txt"
AUTOLEN=30 #urls longer than this automatically get bb'd
url = None 

def shorten(url):
    nurl = API_URL % (LOGIN, API_KEY, urllib.quote(url))
    data = urllib2.urlopen(nurl).read()
    return "{B}Shortened:{B} <{LINK}%s{}>" % data.strip()

def on_PRIVMSG(bot, sender, args):
    global url, AUTOLEN
    PREFIX = '!'
    nick, channel, args = sender.split('!', 1)[0], args[0], args[1]

    cmd = None
    url_re = re.compile('(https?://[^\s]*)')
    res = url_re.search(args)
    curUrl = ""
    if res:
        url = res.groups()[0]
        curUrl = url
    else:
        cmd = args.split(" ")[0]
        curUrl = ""
    
    if len(curUrl)>AUTOLEN or cmd in ['!bb','!bitly', '!short']:
        try: 
            cmd, msg = args.split(' ', 1)
        except ValueError:
            cmd, msg = args, ""
        
        print AUTOLEN,len(url),url, cmd
        bot.say(channel, shorten(url))




