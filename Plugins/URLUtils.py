"""
URL Utilities.
"""

import urllib, urllib2
import re
import lxml.html

URL_RE = re.compile('(https?://[^\s]*)')

def grabTitle(url):
    """Return the title of the page if exists."""
    try:
        page = lxml.html.fromstring(urllib2.urlopen(url).read())
        title = ' '.join(page.head.find('title').text.split())
        if title: 
            return "<{B}Title{}: {C7}%s{}>" % title
    except Exception, e:
        raise e 

def on_PRIVMSG(bot, sender, args, prefix="!"):
    nick, channel, args = sender.split('!', 1)[0], args[0], args[1]

    res = URL_RE.search(args)
    if res: 
        url = res.groups()[0]
        bot.say(channel, grabTitle(url))

