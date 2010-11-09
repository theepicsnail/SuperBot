#!/usr/bin/python
from twisted.words.protocols import irc
from twisted.internet import protocol,reactor 
import sys,traceback,os
from time import time
from Colors import * 


#
#  Consume the error and display an entry in the log
#
def onError():
    et, ev, tb = sys.exc_info()
    t = time()
    red = "\x1b\x5b1;31;40m"
    regular= "\x1b\x5b0;37;40m"
    print "========="+red+"ERROR"+regular+"========"
    print "Time :",t
    last = []         
    skipped= 0
    while tb :
        co = tb.tb_frame.f_code
        filename = str(co.co_filename)
        line_no =  str(traceback.tb_lineno(tb))
        tb = tb.tb_next
        if last!=[filename,line_no]:
            if skipped!=0:
                print "... Skipped",skipped,"repeat(s)."
            print "File :",filename
            print "Line :",line_no
            print "------"
            last=[filename,line_no]
            skipped = 0
        else:
            skipped += 1
    
    if skipped!=0:
        print "... Skipped",skipped,"repeats(s)."
    
    print "Error:",  ev
    print "======================="
    pass


class SuperBot(irc.IRCClient, object):

    def __init__(self):
        global CONFIG
        self.config = CONFIG
        self.plugins=[]
        self.nickname=CONFIG["nick"]
        super(SuperBot,self).__init__()
        global ircColor
        self.ircColor=ircColor
        for i in CONFIG["plugins"]:
            print "Loading",i,
            for n in range(len(i),20):print "",
            if self.loadPlugin(i):
                print "[  OK  ]"
            else:
                print "[FAILED]"
        
    def signedOn(self):
        print "Signed on"
        print "Joining default channels:"
        for i in CONFIG["channels"]:
            print " <%s>"%(i,)
            self.join(i)

    def handleCommand(self,cmd,prefix,params):
        super(SuperBot, self).handleCommand(cmd,prefix,params)
        print "---NORM---"
        print "CMD =",cmd
        print "PRE =",prefix
        print "PAR =",params
        print "----------"*2
        for i in self.plugins:
            try:
                if hasattr(sys.modules[i],"on_"+cmd):
                    getattr(sys.modules[i],"on_"+cmd)(self,prefix,params)
            except Exception as E:
                if hasattr(sys.modules[i],"on_error"):
                    getattr(sys.modules[i],"on_error")(E)
                else:
                    onError()
    
    def ctcpQuery(self,user,chan,mess):
        super(SuperBot,self).ctcpQuery(user,chan,mess)

        cmd = mess[0][0]
        params=mess[0][1]
        print "---CTCP---"
        print cmd
        print user
        print [chan,params]
        print "----------"*2
 
        for i in self.plugins:
            try:
                if hasattr(sys.modules[i],"on_"+cmd):
                    getattr(sys.modules[i],"on_"+cmd)(self,user,[chan,params])
            except:
                onError()
                
                
                
    def loadPlugin(self,name):
        print "Loading",name
        if self.plugins.count(name)!=0:
            print "Plugin Found!, not loading."
            return False
        try:
            print "Plugin not loaded, attempting to load"
            mod = __import__(name)
            print "mod =",mod
            try:
                if hasattr(mod,"on_load"):
                    mod.on_load(self);
            except:
                onError()
            self.plugins.append(name)
            print self.plugins
            return True
        except:
          onError()
        return False
            
    def hasPlugin(self,name):
        return self.plugins.count(name)!=0
    def getPlugins(self):
        return self.plugins

    def unloadPlugin(self,name):
        print "unloadPlugin",name
        if self.plugins.count(name)!=0:

            mod = sys.modules[name]
            print "mod =",mod
            if hasattr(mod,"on_unload"):
                mod.on_unload(self);
            print sys.modules[name]
            del sys.modules[name]

            self.plugins.remove(name)
                
            print mod.__file__
            try:


                os.remove(mod.__file__+"c")
                
            except:
                onError()
            return True
        return False




def loadSettings(config):
    attrs = ["server","port","nick","plugins","channels","pluginDir"]
    listAttrs=["plugins","channels","pluginDir"]
    try:
        settings = dict(l.split(None,1) for l in file(config,"r").readlines())
        for i in attrs:
            if not settings.has_key(i):
                raise Exception("Configure error: '%s' not specified." % (i) )
            
            settings[i] = settings[i].strip()
            if i in listAttrs:
                settings[i]=settings[i].split()
            
    except:
        onError()    
        return
    

    try:
        port = int(settings["port"])
        settings["port"]=port
    except:
        raise Exception("Invalid port number")

    if port < 1 or port > 65535:
        raise Exception("Port value out of range")
    
    print "Configuration:"
    for i in attrs:
        print i,"=>",settings[i]
    return settings





class SuperBotFactory(protocol.ReconnectingClientFactory):
    protocol=SuperBot
    


CONFIG = loadSettings("Config")
if __name__ == "__main__" and CONFIG:
    for i in CONFIG["pluginDir"]:
        sys.path.append(i)
    reactor.connectTCP(CONFIG["server"],CONFIG["port"],SuperBotFactory())
    reactor.run()

