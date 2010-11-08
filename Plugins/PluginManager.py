import thread,os
bot= None

def on_load(b):
    global bot
    bot = b
    if hasattr(b,"reloadList"):
        print "Reload list:",b.reloadList
        for i in b.reloadList:
            if not i == "PluginList":
                b.loadPlugin(i)

def on_NOTICE(connection, nickLine,params):
    source =nickLine.split("!")[0]
    print source
    words = params[1].strip().split(" ")
    colorize = connection.hasPlugin("ColorFilter")
    bold = "{B}" if colorize else ""
    green= "{C}3" if colorize else ""
    red  = "{C}5" if colorize else ""
    none = "{C} " if colorize else ""
    pad = lambda x,y:x+(y-len(x))*" "
    try:
        if words[0]=="plugin":
            if len(words)==3:
                if words[1]=="load":
                    
                    if bot.loadPlugin(words[2]):
                        connection.msg(source,"Load plugin: "+bold+words[2]+bold+green+"loaded.")
                    else:
                        connection.msg(source,"Failed to load "+words[2]+".")
                if words[1]=="unload":
                    if bot.unloadPlugin(words[2]):
                        connection.msg(source,"Plugin "+words[2]+" unloaded.")
                    else:
                        connection.msg(source,"Failed to unload "+words[2]+".")
                if words[1]=="cycle":
                    connection.msg(source,"Cycling "+words[2]);
                    connection.unloadPlugin(words[2])
                    connection.loadPlugin(words[2])
                    connection.msg(source,"Cycle complete")
            else:       
                if len(words)==2:
                    if words[1]=="list":
                        connection.msg(source,"Loaded plugins: "+str(bot.plugins))
            if len(words)==2:
                if words[1]=="update":
                    connection.msg(source,"Updating")
                    print "plug",connection.plugins,bot.plugins
                    print connection.config["pluginDir"]
                    for d in connection.config["pluginDir"]:
                        d = d+ "/"
                        for i in connection.plugins:
                            if os.stat(d+i+".py").st_mtime>os.stat(d+i+".pyc").st_mtime:
                                connection.msg(source,i+" out of date. Reloading.")
                                connection.unloadPlugin(i)
                                connection.loadPlugin(i)
                                connection.msg(source,"Reload complete")
    except TypeError:
        raise
        pass

def restartManager(b):
    print "PluginManager unloaded! Reloading in 5 seconds..."
    from time import sleep
    while True:
        sleep(5)
        b.loadPlugin("PluginManager")
        if b.hasPlugin("PluginManager"):
            print "Plugin manager reloaded"
            print "Loading :",b.reloadList
            for i in b.reloadList:
                b.loadPlugin(i)
            return
        else:
            print "Failed to reload plugin manager! correct error!"
        
def reloader(bot):
    import time
    time.sleep(5)
    bot.loadPlugin("PluginManager")
def on_unload(bot):
    print "Unloading PluginManager..."
    bot.reloadList = list(bot.plugins)
    for plugin in bot.plugins:
        if plugin != "PluginManager":
            print "-- unloading",plugin
            bot.unloadPlugin(plugin)
    thread.start_new_thread(reloader, (bot,))

