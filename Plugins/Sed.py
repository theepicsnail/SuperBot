import re
sed = re.compile("^!s(.)(.*?)\\1(.*?)\\1([gi]{0,2})$")
msgHistory = [""]*10
def on_PRIVMSG(bot,sender,msg):
    global sed,msgHistory
    room,msg = msg

    res = sed.match(msg)
    if res:
        search,replace,flags = res.groups()[1:]
        if flags.find('i')>=0:
            search = re.compile(search, re.I)
        else:
            search = re.compile(search)
        for i in msgHistory:
            res = search.search(i)
            if res:
                if flags.find('g')>=0:
                    bot.say(room,search.sub(replace, i, 0))
                else:
                    bot.say(room,search.sub(replace, i, 1))
                return
    elif msg[0]!="!":
        msgHistory=[msg]+msgHistory[:-1]
