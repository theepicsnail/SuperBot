import tweepy

#Twitter.cfg must contain:

#CONSUMER_KEY=''
#CONSUMER_SECRET=''
#ACCESS_KEY=''
#ACCESS_SECRET=''

execfile("Plugins/Twitter.cfg")

def postUpdate(update):
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)
    status = api.update_status(update)
    print status
    if status: 
        return True

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
                if postUpdate(msg): bot.say(channel, "Update posted.")
            except Exception:
                print Exception

def on_TOPIC(bot,sender,args):
    channel = args[0]
    topic = args[1]
    if postUpdate("Topic: %s"%(topic)):
        bot.say(channel,"Update posted")

