from irclib import *
import traceback,sys
from time import time
class SuperBot(SimpleIRCClient):
    def __init__(self,server,nick):
        SimpleIRCClient.__init__(self)
        self.plugins=[]
        for i in all_events:
            setattr(self, "on_"+i, self.onevent)
        self.connect(server[0],server[1],nick)
        
    def onevent(self,c,e):
        for i in self.plugins:
            try:
                if hasattr(sys.modules[i],"on_"+e.eventtype()):
                    getattr(sys.modules[i],"on_"+e.eventtype())(c,e)
            except:
                et, ev, tb = sys.exc_info()
                t = time()
                print "=========ERROR========"
                print "Time :",t
                
                while tb :
                    co = tb.tb_frame.f_code
                    filename = str(co.co_filename)
                    line_no =  str(traceback.tb_lineno(tb))
                    tb = tb.tb_next
                    print "File :",filename
                    print "Line :",line_no
                    print "------"
                
                c.privmsg(nm_to_n(e.source()),"An error occured! "+filename+":"+line_no+" - "+str(ev)+" - id:"+str(t))
                print "Error:",  ev
                raise
                
        
    def loadPlugin(self,name):
        print "Loading",name
        if self.plugins.count(name)!=0:
            print "Found!, not loading."
            return False
        try:
            mod = __import__(name)
            if hasattr(mod,"on_load"):
                mod.on_load(self);
            self.plugins.append(name)
            return True
        except:
            return False
        
        
    def unloadPlugin(self,name):
        print "unloadPlugin",name
        if self.plugins.count(name)!=0:

            mod = sys.modules[name]
            if hasattr(mod,"on_unload"):
                mod.on_unload(self);

            del sys.modules[name]
            self.plugins.remove(name)
                            
            try:
                # if it came from asdf.py, remove asdf.pyc (to ensure next load is fresh)
                # if it came from asdf.pyc, remove asdf.pycc which shouldn't exist, and will be ignored
                os.remove(sys.modules[name].__file__+"c")
            except:
                pass
                
            
            return True
        return False
def main(settings):
    bot = SuperBot((settings["server"],settings["port"]),settings["nick"])
    for i in settings["plugins"]:
        print "Loading",i,
        for n in range(len(i),20):print "",
        if bot.loadPlugin(i):
            print "[  OK  ]"
        else:
            print "[FAILED]"
    bot.start()

def loadSettings(config):
    try:
        settings = dict(l.split(None,1) for l in file(config,"r").readlines())
        for i in ["server","port","nick","plugins"]:
            if not settings.has_key(i):
                raise Exception(" %1% not specified." % (i) )

            if i=="plugins":
                settings[i]=settings[i].split()
            else:
                settings[i]=settings[i].strip()
    except ValueError, v:
        print vs
        parts = v.message.replace("#"," ").replace(";"," ").split(" ")
        raise Exception("Error on line "+str(int(parts[5])+1))
    
    

    try:
        port = int(settings["port"])
        settings["port"]=port
    except:
        raise Exception("Invalid port number")

    if port < 1 or port > 65535:
        raise Exception("Port value out of range")
    
    print "Configuration:"
    for i in ["server","port","nick","plugins"]:
        print i,"=>",settings[i]
    return settings

if __name__ == "__main__":
    config = "Config"
    #try:
    settings = loadSettings(config)
    main(settings)
    #except Exception, e:
        #print "====Configure Error===="
        #print e
        #raise e
    