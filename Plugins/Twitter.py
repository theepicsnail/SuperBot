import twitter

twit_password = file("Twitter-private","r").readlines()[0].strip()

def postUpdate(user, update):
    #OLD COMMENT IS OLD - #hardcoded password sucks! but maybe in the future we can accept pm's with ppls passwords and they can post to twitter from here =)
    # The password is no less hardcoded now, but at least it's in a seperate file.
    api = twitter.Api(username=user, password=twit_password)
    if api.PostUpdate(update): return True

def getLatestStatus(user):
    api = twitter.Api()
    statuses = api.GetUserTimeline(user)
    return statuses[0].text


def on_PRIVMSG(bot, sender, args):
    PREFIX = '!'
    nick, channel, args = sender.split('!', 1)[0], args[0], args[1]
    
    if args.startswith(PREFIX):
        try: 
            cmd, msg = args.split(' ', 1)  
        except ValueError:
            cmd, msg = args, ""
        if cmd == '!tweet' and msg:
            try:
                user = msg.split('<')[0]
                update = msg.split('<')[1]
                if postUpdate(user, update): bot.say(channel, "Update posted.")
            except Exception:
                print Exception
            bot.say(channel, getLatestStatus(msg))




