"""
URL Utilities.
"""

import urllib, urllib2
import re

URL_RE = re.compile('(https?://[^\s]*)')

def grabTitle(url):
    """Return the title of the page if exists."""
    try:
        title = urllib2.urlopen(url, None, 5).read(5120).split("title>")[1][:-2]
        title = re.sub('[\n\r\t ]+', ' ', title).strip()
        unicode(title, errors='ignore')
        if title: 
            return "<{B}Title{}: {C7}%s{}>" % title
    except Exception, e:
        raise e

def on_PRIVMSG(bot, sender, args, prefix="!"):
    nick, channel, args = sender.split('!', 1)[0], args[0], args[1]

    res = URL_RE.search(args)
    if res && nick != 'Pixel':
        url = res.groups()[0]
        bot.say(channel, grabTitle(url))
