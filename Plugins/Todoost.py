import urllib2
def on_PRIVMSG(bot,nick,msg):
    source = msg[0]
    if source == bot.nickname:
        source = nick.split("!")[0]
    cmd = msg[1].split()
    if cmd[0]=="!todoost": 
        if len(cmd) != 2:
            bot.say(source,"Usage: !todoost listName")
        else:
            doTodoost(bot,source,cmd[1])

def taskCompleted(task):
    return task.split("</a>")[0].endswith("X")
def taskName(task):
    return task.split("</a>")[1].split(">")[-1]
def doTodoost(bot,chan, p):
    page = "http://%s.todoost.com"%p
    data = urllib2.urlopen(page).read()
    tasks = data.split("<li class=")[1:]
    comp = filter(taskCompleted,tasks)
    nextTask = "None"
    for i in tasks:
        if not taskCompleted(i):
            nextTask = taskName(i)
            break 
    bot.say(chan,"Completed %i of %i task(s). Next up: %s."%(len(comp),len(tasks),nextTask))
    
