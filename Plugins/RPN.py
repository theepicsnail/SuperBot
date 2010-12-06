
commands={
"+":lambda stk:stk.pop()+stk.pop(),
"*":lambda stk:stk.pop()*stk.pop(),
"-":lambda stk:-stk.pop() + stk.pop(),
"/":lambda stk:1/stk.pop() * stk.pop()

}

def on_load(b):
    pass
def on_unload(bot):
    pass
def on_PRIVMSG(bot, sender, args):
    nick, channel, msg = sender.split('!', 1)[0], args[0], args[1]
    parts = msg.split()
    if len(parts)==0: return
    if parts[0]!="!rpn": return
    
    stk=[]
    
    for part in parts[1:]:
        if part in commands:
            
            stk.append(commands[part](stk))
        else:
            try:
                stk.append(float(part))
            except:
                bot.say(channel,"Error parsing: "+part)
                return
    if len(stk)==1:
        bot.say(channel,str(stk.pop()))
    else:
        bot.say(channel,str(stk))
