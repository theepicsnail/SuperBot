import BaseHTTPServer
import threading
import json
from urllib import unquote_plus
running = True
bot = None
channel="#adullam"

def on_load(b):
    global bot
    bot = b
    WebThread().start()
    
def on_unload(bot):
    global running
    running = False    

class Handler(BaseHTTPServer.BaseHTTPRequestHandler ):
    def do_GET(self):#doing a get does nothing
        self.sendPage("text/html","<html></html>")
#        global bot
#        bot.handleWeb("GET",self)

    def do_POST(self):
        self.sendPage("text/html","<html></html>")
        handleWeb(self)

    def sendPage(self,type,body):
        self.send_response(200)
        self.send_header("Content-type",type)
        self.send_header("Content-length",str(len(body)))
        self.end_headers()
        self.wfile.write(body)


class WebThread (threading.Thread):
    def run(self):
        global running
        server = BaseHTTPServer.HTTPServer(('',8000),Handler)
        while running:
            server.handle_request()
            print running

def handleWeb(data):
    try:
        global count,bot
        if data.headers.has_key("content-length"):
            l = data.headers["content-length"]
            l = int(l)
            data = unquote_plus(data.rfile.read(l)).split("=")[1]
            jo= json.JSONDecoder().decode(data)
            comm= jo["commits"][0]
            msg = "{C2}[Commit] {C3}"+comm["author"]["username"]
            msg += "{C7} " + comm["message"]
            msg += "{C6} " + comm["timestamp"]
            msg = msg.encode("utf-8")
    #            print jo["commits"]["author"]["username"], jo["commits"]["message"], jo["commits"]["timestamp"] 
    #        if count == 0:
            global bot
            print "Channel:",channel
            print "Message:",msg
            
            bot.say(channel,msg)
            bot.transport.doWrite() #this is in a different thread i guess?
    except:
        raise


