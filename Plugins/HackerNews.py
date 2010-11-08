"""
HackerNews plugin for Superbot.
Able to retrieve latest/best hacker news stories.
"""
import urllib, urllib2
from Google import _buildResponse, HEADERS
import lxml.html
import re

BEST_URL = "http://news.ycombinator.com/best"
NEWEST_URL = "http://news.ycombinator.com/newest"
CURRENT_URL = "http://news.ycombinator.com/"

def best(num=0):
    response = _buildResponse(BEST_URL)
    html = response.read()
    pdoc = lxml.html.fromstring(html)
    results = [t for t in pdoc.body.cssselect('table tr td.title a')]
    result = results[num]
    title = result.text_content()
    href= result.attrib['href']
    return "<{C8}%s{} | {LINK}%s{}>  {C13}[%s of %s]{}" % (title, href, num, len(results)-1)

def newest(num=0):
    response = _buildResponse(NEWEST_URL)
    html = response.read()
    pdoc = lxml.html.fromstring(html)
    results = [t for t in pdoc.body.cssselect('table tr td.title a')]
    result = results[num]
    title = result.text_content()
    href= result.attrib['href']
    return "<{C8}%s{} | {LINK}%s{}>  {C13}[%s of %s]{}" % (title, href, num, len(results)-1)


def current(num=0):
    response = _buildResponse(CURRENT_URL)
    html = response.read()
    pdoc = lxml.html.fromstring(html)
    results = [t for t in pdoc.body.cssselect('table tr td.title a')]
    result = results[num]
    title = result.text_content()
    href= result.attrib['href']
    return "<{C8}%s{} | {LINK}%s{}>  {C13}[%s of %s]{}" % (title, href, num, len(results)-1)

def search(query, num=0):
    #only search current for now 
    response = _buildResponse(CURRENT_URL)
    html = response.read()
    pdoc = lxml.html.fromstring(html)
    results = [t for t in pdoc.body.cssselect('table tr td.title a')]
    
    d = dict([(result.attrib['href'],result.text_content()) for result in results])
    
    search_re = re.compile('%s' % query, re.I)
    
    matches = []
    
    for href,text in d.items():
        if search_re.search(text):
            matches.append("<{C8}%s{} | {LINK}%s{}>" % (text,href))

    if not len(matches): return "No results found. =("
    
    return matches[num] + " {C13}[%s of %s]{}" % (num, len(matches)-1)


def on_PRIVMSG(bot, sender, args):
    PREFIX = '!'
    nick, channel, args = sender.split('!', 1)[0], args[0], args[1]
    
    if args.startswith(PREFIX):
        try:
            cmd, msg = args.split(' ', 1)
        except ValueError:
            cmd, msg = args, ""
        if cmd in ["!hn", "!hackernews"]:
            if len(msg.split()) >= 2 and msg.split()[0] == 'search':
                try:
                    if int(msg.split()[-1]):
                        num = int(msg.split().pop())
                        query = ' '.join(msg.split()[1:-1])
                except ValueError:
                    num = 0
                    query = ' '.join(msg.split()[1:])
                bot.say(channel, search(query, num))
            try:
                which, num = msg.split()
                num = int(num)
            except ValueError:
                which, num = msg, 0
            
            if which == "best": bot.say(channel, best(num))
            if which == "newest": bot.say(channel, newest(num))
            if which == "current": bot.say(channel, current(num))
 


