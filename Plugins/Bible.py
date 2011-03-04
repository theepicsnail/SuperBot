"""Bible plugin."""

import lxml.html
import urllib2


def bible(book, chapter, verse):
    url = "http://api.preachingcentral.com/bible.php?passage=%s%s:%s&version=asv" % (book, chapter, verse)
    parsed = lxml.html.fromstring(urllib2.urlopen(url).read())
    b = parsed.find('range').find('item').find('bookname').text_content()
    c = parsed.find('range').find('item').find('chapter').text_content()
    v = parsed.find('range').find('item').find('verse').text_content() 
    t = parsed.find('range').find('item').find('text').text_content() 
    return "<{C4}{B}%s %s:%s{}: {B}%s{}>" % (b, c, v, t)

def on_PRIVMSG(bot, sender, args):
    nick, channel, args = sender.split('!', 1)[0], args[0], args[1]

    if args.startswith("!"):
        try: 
            cmd, msg = args.split(' ', 1)
        except ValueError:
            cmd, msg = args, ""
 
        if cmd in ['!bible']:
            args = args.split()
            book, chap, verse = args[1], args[2].split(':')[0], args[2].split(':')[1]
            bot.say(channel, bible(book, chap, verse))    
    



