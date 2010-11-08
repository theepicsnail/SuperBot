"""URL Shortening via the Bitly API for use within IRC"""

import urllib2
import re
import urllib

LOGIN = "tsoporan"
API_KEY = "R_e29b3e8186e3fec26cbb30963dfc3747"
API_URL = "http://api.bit.ly/v3/shorten?login=%s&apiKey=%s&longUrl=%s&format=txt"
url = None 

def shorten(url):
    nurl = API_URL % (LOGIN, API_KEY, urllib.quote(url))
    data = urllib2.urlopen(nurl).read()
    return "{B}Shortened:{B} <{LINK}%s{}>" % data.strip()

def on_PRIVMSG(bot, sender, args):
    global url 
    PREFIX = '!'
    nick, channel, args = sender.split('!', 1)[0], args[0], args[1]

    url_re = re.compile('(https?://[^\s]*)')
    res = url_re.search(args)
    if res:
        url = res.groups()[0]

    if args.startswith(PREFIX) and url:
        try: 
            cmd, msg = args.split(' ', 1)
        except ValueError:
            cmd, msg = args, ""
        
        if cmd in ['!bb','!bitly', '!short']:
            bot.say(channel, shorten(url))



