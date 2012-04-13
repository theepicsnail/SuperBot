import urllib2
import re
import urllib
import socket
import thread
from time import sleep

items = [['0', 'Air'], ['1', 'Stone'], ['2', 'Grass'], ['3', 'Dirt'], ['4', 'Cobblestone'], ['5', 'Wooden Plank'], ['6', 'Sapling'], ['6:1', 'Redwood Sapling'], ['6:2', 'Birch Sapling'], 
        ['7', 'Bedrock'], ['8', 'Water'], ['9', 'Stationary Water'], ['10', 'Lava'], ['11', 'Stationary Lava'], ['12', 'Sand'], ['13', 'Gravel'], ['14', 'Gold Ore'], ['15', 'Iron Ore'], 
        ['16', 'Coal Ore'], ['17', 'Wood'], ['17:1', 'Redwood'], ['17:2', 'Birchwood'], ['18', 'Leaves'], ['18:1', 'Redwood Leaves'], ['18:2', 'Birchwood Leaves'], ['19', 'Sponge'], ['20', 'Glass'],
        ['21', 'Lapis Lazuli Ore'], ['22', 'Lapis Lazuli Block'], ['23', 'Dispenser'], ['24', 'Sandstone'], ['25', 'Note Block'], ['26', 'Bed Block'], ['27', 'Powered Rail'], ['28', 'Detector Rail'],
        ['29', 'Sticky Piston'], ['30', 'Web'], ['31', 'Dead Shrub'], ['31:1', 'Tall Grass'], ['31:2', 'Live Shrub'], ['32', 'Dead Shrub'], ['33', 'Piston'], ['34', 'Piston Head'], 
        ['35', 'White Wool'], ['35:1', 'Orange Wool'], ['35:2', 'Magenta Wool'], ['35:3', 'Light Blue Wool'], ['35:4', 'Yellow Wool'], ['35:5', 'Light Green Wool'], ['35:6', 'Pink Wool'], 
        ['35:7', 'Gray Wool'], ['35:8', 'Light Gray Wool'], ['35:9', 'Cyan Wool'], ['35:10', 'Purple Wool'], ['35:11', 'Blue Wool'], ['35:12', 'Brown Wool'], ['35:13', 'Dark Green Wool'], 
        ['35:14', 'Red Wool'], ['35:15', 'Black Wool'], ['37', 'Yellow Flower'], ['38', 'Red Rose'], ['39', 'Brown Mushroom'], ['40', 'Red Mushroom'], ['41', 'Gold Block'], ['42', 'Iron Block'], 
        ['43', 'Double Stone Slab'], ['43:1', 'Double Sandstone Slab'], ['43:2', 'Double Wooden Slab'], ['43:3', 'Double Cobblestone Slab'], ['44', 'Stone Slab'], ['44:1', 'Sandstone Slab'], 
        ['44:2', 'Wooden Slab'], ['44:3', 'Cobblestone Slab'], ['45', 'Brick'], ['46', 'TNT'], ['47', 'Bookshelf'], ['48', 'Mossy Cobblestone'], ['49', 'Obsidian'], ['50', 'Torch'], ['51', 'Fire'], 
        ['52', 'Monster Spawner'], ['53', 'Wooden Stairs'], ['54', 'Chest'], ['55', 'Redstone Wire'], ['56', 'Diamond Ore'], ['57', 'Diamond Block'], ['58', 'Workbench'], ['59', 'Crops'], 
        ['60', 'Soil'], ['61', 'Furnace'], ['62', 'Burning Furnace'], ['63', 'Sign Post'], ['64', 'Wooden Door'], ['65', 'Ladder'], ['66', 'Rails'], ['67', 'Cobblestone Stairs'], ['68', 'Wall Sign'],
        ['69', 'Lever'], ['70', 'Stone Pressure Plate'], ['71', 'Iron Door'], ['72', 'Wooden Pressure Plate'], ['73', 'Redstone Ore'], ['74', 'Glowing Redstone Ore'], ['75', 'Redstone Torch (off)'],
        ['76', 'Redstone Torch (on)'], ['77', 'Stone Button'], ['78', 'Snow'], ['79', 'Ice'], ['80', 'Snow Block'], ['81', 'Cactus'], ['82', 'Clay'], ['83', 'Sugar Cane'], ['84', 'Jukebox'],
        ['85', 'Fence'], ['86', 'Pumpkin'], ['87', 'Netherrack'], ['88', 'Soul Sand'], ['89', 'Glowstone'], ['90', 'Portal'], ['91', 'Jack-O-Lantern'], ['92', 'Cake Block'], 
        ['93', 'Redstone Repeater Block (off)'], ['94', 'Redstone Repeater Block (on)'], ['95', 'Locked Chest'], ['96', 'Trapdoor'], ['256', 'Iron Shovel'], ['257', 'Iron Pickaxe'], 
        ['258', 'Iron Axe'], ['259', 'Flint and Steel'], ['260', 'Apple'], ['261', 'Bow'], ['262', 'Arrow'], ['263', 'Coal'], ['263:1', 'Charcoal'], ['264', 'Diamond'], ['265', 'Iron Ingot'], 
        ['266', 'Gold Ingot'], ['267', 'Iron Sword'], ['268', 'Wooden Sword'], ['269', 'Wooden Shovel'], ['270', 'Wooden Pickaxe'], ['271', 'Wooden Axe'], ['272', 'Stone Sword'], 
        ['273', 'Stone Shovel'], ['274', 'Stone Pickaxe'], ['275', 'Stone Axe'], ['276', 'Diamond Sword'], ['277', 'Diamond Shovel'], ['278', 'Diamond Pickaxe'], ['279', 'Diamond Axe'], 
        ['280', 'Stick'], ['281', 'Bowl'], ['282', 'Mushroom Soup'], ['283', 'Gold Sword'], ['284', 'Gold Shovel'], ['285', 'Gold Pickaxe'], ['286', 'Gold Axe'], ['287', 'String'], 
        ['288', 'Feather'], ['289', 'Sulphur'], ['290', 'Wooden Hoe'], ['291', 'Stone Hoe'], ['292', 'Iron Hoe'], ['293', 'Diamond Hoe'], ['294', 'Gold Hoe'], ['295', 'Seeds'], ['296', 'Wheat'], 
        ['297', 'Bread'], ['298', 'Leather Helmet'], ['299', 'Leather Chestplate'], ['300', 'Leather Leggings'], ['301', 'Leather Boots'], ['302', 'Chainmail Helmet'], 
        ['303', 'Chainmail Chestplate'], ['304', 'Chainmail Leggings'], ['305', 'Chainmail Boots'], ['306', 'Iron Helmet'], ['307', 'Iron Chestplate'], ['308', 'Iron Leggings'], 
        ['309', 'Iron Boots'], ['310', 'Diamond Helmet'], ['311', 'Diamond Chestplate'], ['312', 'Diamond Leggings'], ['313', 'Diamond Boots'], ['314', 'Gold Helmet'], ['315', 'Gold Chestplate'], 
        ['316', 'Gold Leggings'], ['317', 'Gold Boots'], ['318', 'Flint'], ['319', 'Raw Porkchop'], ['320', 'Cooked Porkchop'], ['321', 'Painting'], ['322', 'Golden Apple'], ['323', 'Sign'], 
        ['324', 'Wooden Door'], ['325', 'Bucket'], ['326', 'Water Bucket'], ['327', 'Lava Bucket'], ['328', 'Minecart'], ['329', 'Saddle'], ['330', 'Iron Door'], ['331', 'Redstone'], 
        ['332', 'Snowball'], ['333', 'Boat'], ['334', 'Leather'], ['335', 'Milk Bucket'], ['336', 'Clay Brick'], ['337', 'Clay Balls'], ['338', 'Sugarcane'], ['339', 'Paper'], ['340', 'Book'], 
        ['341', 'Slimeball'], ['342', 'Storage Minecart'], ['343', 'Powered Minecart'], ['344', 'Egg'], ['345', 'Compass'], ['346', 'Fishing Rod'], ['347', 'Clock'], ['348', 'Glowstone Dust'], 
        ['349', 'Raw Fish'], ['350', 'Cooked Fish'], ['351', 'Ink Sack'], ['351:1', 'Rose Red'], ['351:2', 'Cactus Green'], ['351:3', 'Coco Beans'], ['351:4', 'Lapis Lazuli'], 
        ['351:5', 'Purple Dye'], ['351:6', 'Cyan Dye'], ['351:7', 'Light Gray Dye'], ['351:8', 'Gray Dye'], ['351:9', 'Pink Dye'], ['351:10', 'Lime Dye'], ['351:11', 'Dandelion Yellow'], 
        ['351:12', 'Light Blue Dye'], ['351:13', 'Magenta Dye'], ['351:14', 'Orange Dye'], ['351:15', 'Bone Meal'], ['352', 'Bone'], ['353', 'Sugar'], ['354', 'Cake'], ['355', 'Bed'], 
        ['356', 'Redstone Repeater'], ['357', 'Cookie'], ['358', 'Map'], ['359', 'Shears'], ['2256', 'Gold Music Disc'], ['2257', 'Green Music Disc']]


items = map(lambda x:[x[0],x[1].lower()],items)

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
        return res[0][0]
    if len(res) > 1:
        lst = ", ".join(map(lambda x:" ".join(x[1:]),res))

        toMinecraft("Multiple matches: "+lst)
        return None
def give(player,name,quant=1):
    try:
        print "give",player,name,quant
        num = None
        try:
            num = int(name)
        except:
            num = search(name)
        print num

        if num == None:
            raise Exception()

        qnt = int(quant)
        print qnt
        global mc
        while qnt>0:
            mc.send("give %s %s %s\n"%(player,num,qnt))
            qnt -= 64

    except:
        toMinecraft("Give failed.")





bot = None
mc = None
running = False
def on_load(b):
    b.join("#mc")
    global bot,mc,running
    bot = b
    mc = socket.socket()  
#    bot.say("#adullam","Connecting to minecraft") 
    try:
        mc.connect(("gene.indstate.edu",10240))
        running = True
#        bot.say("#adullam","Connected!")
        toMinecraft("Plugin activated")
        thread.start_new_thread(mcThread,(None,))
    except e:
        bot.say("#adullam","Failed to connect")
        raise e
def Lookup(shorthand):
    print "Lookup:",shorthand
    mc.send("list\n")
    resp = mc.recv(1024)
    if "Connected players:" not in resp:
        toMinecraft("Something strange happend...")
        toMinecraft(resp)
        return shorthand
    players = resp.split("players:")[1].replace(",","").split()
    matches = filter(lambda x:shorthand in x, players)
    if len(matches)==1:
        return matches[0]
    if len(matches)>1:
        toMinecraft("Matches: %r"%matches)
    if len(matches)==0:
        toMinecraft("No matches.")
    return shorthand
        
def TP(src,dst):
    mc.send("tp {} {}\n".format(src,dst))
def mcThread(args):
    global running,mc,bot
    buffer = ""
    
    while running:
        tmp = mc.recv(100)
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
            
            tp = re.match("!tp (.*) (.*)$",msg)
            if tp:
                TP(Lookup(tp.groups()[0]),Lookup(tp.groups()[1]))
                continue

            tp = re.match("!tp (.*)$",msg)
            if tp:
                TP(g[0],Lookup(tp.groups()[0]))
                continue
                
            cheats = """
            id = re.match("!id (.*)",msg)
            if id:
                search(id.groups()[0])
                continue
            gi = re.match("!give (.*) (.*)",msg)
            if gi:
                give(g[0],*gi.groups())
                continue

            ar = re.match("!armor", msg)
            if ar:
                give(g[0],"diamond helmet")
                give(g[0],"diamond chestplate")
                give(g[0],"diamond legging")
                give(g[0],"diamond boots")
            """#"""
            
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




