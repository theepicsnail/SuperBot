
#/tmp/superbot.pid
#/tmp/tehorngdata
superbot = None
def tehorng(*a):
    global superbot
    if superbot:
        f=file("/tmp/tehorngdata")
        if f:
            superbot.say("#adullam", f.read())
        else:
            print "Caught signal, no /tmp/tehorngdata though :(";
    else:
        print "Caught signal no superbot though? lol wtf"
def cycler(*a):
    print "caught signal usr2, cycling updated plugins"
    global superbot
    if superbot:
        for d in superbot.config["pluginDir"]:
            d = d+ "/"
            for i in superbot.plugins:
                print "Checking",i,
                if os.stat(d+i+".py").st_mtime>os.stat(d+i+".pyc").st_mtime:
                    print "cycling"
                    superbot.unloadPlugin(i)
                    superbot.loadPlugin(i)
                    print "cycle complete"
                else:
                    print "up to date"
        
import signal,os
signal.signal( signal.SIGUSR1, tehorng)
signal.signal( signal.SIGUSR2, cycler)
def on_load(bot):
    global superbot
    superbot=bot
    file("/tmp/superbot.pid","w").write(str(os.getpid()))
def on_unload(bot):
    os.remove("/tmp/superbot.pid")
    
