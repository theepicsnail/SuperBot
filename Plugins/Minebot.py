import urllib2
import re
import urllib
import socket
import thread
from time import sleep


items = [[0, 'air'], [1, 'stone'], [2, 'grass'], [3, 'dirt'], [4, 'cobblestone'], [5, 'wood'], [6, 'sapling'], [7, 'bedrock'], [8, 'water'], [9, 'stationary', 'water'], [10, 'lava'], [11, 'stationary', 'lava'], [12, 'sand'], [13, 'gravel'], [14, 'gold', 'ore'], [15, 'iron', 'ore'], [16, 'coal', 'ore'], [17, 'log'], [18, 'leaves'], [19, 'sponge'], [20, 'glass'], [21, 'red', 'cloth'], [22, 'orange', 'cloth'], [23, 'yellow', 'cloth'], [24, 'lime', 'cloth'], [25, 'green', 'cloth'], [26, 'aqua', 'green', 'cloth'], [27, 'cyan', 'cloth'], [28, 'blue', 'cloth'], [29, 'purple', 'cloth'], [30, 'indigo', 'cloth'], [31, 'violet', 'cloth'], [32, 'magenta', 'cloth'], [33, 'pink', 'cloth'], [34, 'black', 'cloth'], [35, 'gray', 'cloth', '/', 'white', 'cloth'], [36, 'white', 'cloth'], [37, 'yellow', 'flower'], [38, 'red', 'rose'], [39, 'brown', 'mushroom'], [40, 'red', 'mushroom'], [41, 'gold', 'block'], [42, 'iron', 'block'], [43, 'double', 'step'], [44, 'step'], [45, 'brick'], [46, 'tnt'], [47, 'bookshelf'], [48, 'mossy', 'cobblestone'], [49, 'obsidian'], [50, 'torch'], [51, 'fire'], [52, 'mob', 'spawner'], [53, 'wooden', 'stairs'], [54, 'chest'], [55, 'redstone', 'wire'], [56, 'diamond', 'ore'], [57, 'diamond', 'block'], [58, 'workbench'], [59, 'crops'],
[60, 'soil'], [61, 'furnace'], [62, 'burning', 'furnace'], [63, 'sign', 'post'], [64, 'wooden', 'door'], [65, 'ladder'], [66, 'minecart', 'tracks'], [67, 'cobblestone', 'stairs'], [68, 'wall', 'sign'], [69, 'lever'], [70, 'stone', 'pressure', 'plate'], [71, 'iron', 'door'], [72, 'wooden', 'pressure', 'plate'], [73, 'redstone', 'ore'], [74, 'glowing', 'redstone', 'ore'], [75, 'redstone', 'torch', '("off"', 'state)'], [76, 'redstone', 'torch', '("on"', 'state)'], [77, 'stone', 'button'], [78, 'snow'], [79, 'ice'], [80, 'snow', 'block'], [81, 'cactus'], [82, 'clay'], [83, 'reed'], [84, 'jukebox'], [85, 'fence'], [256, 'iron', 'spade'], [257, 'iron', 'pickaxe'], [258, 'iron', 'axe'], [259, 'flint', 'and', 'steel'], [260, 'apple'], [261, 'bow'], [262, 'arrow'], [263, 'coal'], [264, 'diamond'], [265, 'iron', 'ingot'], [266, 'gold', 'ingot'], [267, 'iron', 'sword'], [268, 'wooden', 'sword'], [269, 'wooden', 'spade'], [270, 'wooden', 'pickaxe'], [271, 'wooden', 'axe'], [272, 'stone', 'sword'], [273, 'stone', 'spade'], [274, 'stone', 'pickaxe'], [275, 'stone', 'axe'], [276, 'diamond', 'sword'], [277, 'diamond', 'spade'], [278, 'diamond', 'pickaxe'], [279, 'diamond', 'axe'], [280, 'stick'], [281, 'bowl'], [282, 'mushroom', 'soup'], [283, 'gold', 'sword'], [284, 'gold', 'spade'], [285, 'gold', 'pickaxe'], [286, 'gold', 'axe'], [287, 'string'], [288, 'feather'], [289, 'gunpowder'],
[290, 'wooden', 'hoe'], [291, 'stone', 'hoe'], [292, 'iron', 'hoe'], [293, 'diamond', 'hoe'], [294, 'gold', 'hoe'], [295, 'seeds'], [296, 'wheat'], [297, 'bread'], [298, 'leather', 'helmet'], [299, 'leather', 'chestplate'], [300, 'leather', 'pants'], [301, 'leather', 'boots'], [302, 'chainmail', 'helmet'], [303, 'chainmail', 'chestplate'], [304, 'chainmail', 'pants'], [305, 'chainmail', 'boots'], [306, 'iron', 'helmet'], [307, 'iron', 'chestplate'], [308, 'iron', 'pants'], [309, 'iron', 'boots'], [310, 'diamond', 'helmet'], [311, 'diamond', 'chestplate'], [312, 'diamond', 'pants'], [313, 'diamond', 'boots'], [314, 'gold', 'helmet'], [315, 'gold', 'chestplate'], [316, 'gold', 'pants'], [317, 'gold', 'boots'], [318, 'flint'], [319, 'pork'], [320, 'grilled', 'pork'], [321, 'paintings'], [322, 'golden', 'apple'], [323, 'sign'], [324, 'wooden', 'door'], [325, 'bucket'], [326, 'water', 'bucket'], [327, 'lava', 'bucket'], [328, 'mine', 'cart'], [329, 'saddle'], [330, 'iron', 'door'], [331, 'redstone'], [332, 'snowball'], [333, 'boat'], [334, 'leather'], [335, 'milk', 'bucket'], [336, 'clay', 'brick'], [337, 'clay', 'balls'], [338, 'reed'], [339, 'paper'], [340, 'book'], [341, 'slime', 'ball'], [342, 'storage', 'minecart'], [343, 'powered', 'minecart'], [344, 'egg'], [345, 'compass'], [346, 'fishing', 'rod'], [2256, 'gold', 'record'], [2257, 'green', 'record']]



def search(name):
    name = name.lower()
    match = lambda i:name in str(" ".join(i[1:]))
    exact = lambda i:name == str(" ".join(i[1:]))
    res = filter(match,items)
    if not res:
        toMinecraft("No items found")
        return
    sres = filter(exact,items)
    if sres or len(res)==1:
        toMinecraft("ID: "+str(res[0]))
    if len(res) > 1:
        lst = ", ".join(map(lambda x:" ".join(x[1:]),res))

        toMinecraft("Multiple matches: "+lst)
    





bot = None
mc = None
running = False
def on_load(b):
    b.join("#mc")
    global bot,mc,running
    bot = b
    mc = socket.socket()  
    bot.say("#adullam","Connecting to minecraft") 
    try:
        mc.connect(("gene.indstate.edu",10240))
        running = True
        bot.say("#adullam","Connected!")
        toMinecraft("Plugin activated")
        thread.start_new_thread(mcThread,(None,))
    except e:
        bot.say("#adullam","Failed to connect")
        raise e

def mcThread(args):
    global running,mc,bot
    buffer = ""
    
    while running:
        tmp = mc.recv(1)
        buffer += tmp
        if not tmp or buffer.count("\n")==0:
            continue
        
        line,buffer=buffer.split("\n",1)
        msg = re.match("^.*INFO] <(.*)> (.*)$",line)
        if msg:
            g = msg.groups()
            toAdullam = g[1].startswith("t ")
            msg = g[1]
            if toAdullam:
                msg=g[1][2:]
            id = re.match("!id (.*)",msg)
            if id:
                search(id.groups()[0])
                continue
#            give = re.match("!give (.*) (.*)")

            toIRC("{C2}"+g[0][:-1]+"_:{} "+msg,toAdullam)
            continue
        
        login = re.match("^.*INFO] (.*) .* .*logged in$",line)
        if login:
            g=login.groups()
            toIRC("{C2}"+g[0]+" {}logged in.")
            
        plist = re.match("^.*INFO] Connected players:(.*)$",line)
        if plist:
            g = plist.groups()
            toIRC("{C2}Connected players:{}"+g[0])

        logout = re.match("^.*INFO] (.*) lost connection.*",line)
        if logout:
            msg = "logged out."
            if line.count("Internal exception") or line.count("End of stream"):
                g = logout.groups()
                msg = "crashed!"
                toMinecraft(g[0]+" crashed!")
            toIRC("{C2}"+g[0]+" {}"+msg)
            
        
def on_unload(bot):
    global running,mc
    print "Minebot unloaded"
    running=False
    mc.close()
    bot.part("#mc")

def toIRC(msg, adu=False):
    global bot
    print "Sent: "+msg
    if adu:
        bot.say("#adullam","[{C3}MC{}]"+msg)
    bot.say("#mc",msg)
    bot.transport.doWrite()

def toMinecraft(msg):
    global mc
    if mc:
        mc.send("say "+msg+"\n")

def on_PRIVMSG(bot, sender, args):
    global url 
    PREFIX = '!'
    nick, channel, args = sender.split('!', 1)[0], args[0], args[1]
    print "Chan:", channel
    if not channel in ["#adullam", "#mc"]:
        return
    
    argList = args.split(" ")
    if argList[0]=="!mc":
        if len(argList)==1:
            toIRC("!mc [cmd] (cmds are 'list' and 'tp')")
            return
        if argList[1]=="list":
            mc.send("list\n")
        if argList[1]=="tp":
            if len(argList)!=4:
                toIRC("!mc tp person targetPerson")
                return
            mc.send(args.split(" ",1)[1]+"\n")
            
    else:
        toMinecraft("["+channel[1:]+"] <"+nick+">"+args)




