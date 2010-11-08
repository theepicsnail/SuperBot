table=[
    ['jizz', '[vanilla pudding]'], ['sex', 'secks'], ['vista', '[I like manginas]'], ['pussy', '[cute kitty]'], 
    ['prick', '[tool to pick things]'], ['damn', '[Hoover Dam]'], ['whore', '[Hillary Duff]'], ['lesbian', '[Britney Spears]'], 
    ['slut', '[Bill Clinton]'], ['shit', '[doodie ball]'], ['ass', '[donkey]'], ['bitch', '[carpenter]'], ['cock', '[adoodledo]'], 
    ['dick', '[phallic male genitalia of the penile organ genus]'], ['cunt', '[introverted phallic female genitalia of the vaginile organ genus]'], 
    ['twat', '[holy elixir of life]'], ['vagina', '[sandbox]'], ['penis', '[man-meat]'], ['jackass', '[Jerky McJerkface]'], ['fucker', '[felcher]'], 
    ['horny', '[enamoured]'], ['gay', '[happy, happy, joy, joy]'], ['dickhead', '[Poopy McStupidHead]'], ['fuck', '[sexual intercourse]'], 
    ['microsoft', '[The Antichrist Company]'], ['windows', '[WinBlowZ]'], ['dyke', '[Dick van Dyke Show]'], ['kyke', '[matzoh-ball]'], 
    ['kike', '[matzoh-ball]'], ['nigger', '[brother]'], ['penetration', '[farketration]'], ['oral sex', '[oral surgery]'], ['blowjob', '[farkjob]'], 
    ['fisting', '[farting]'], ['asshole', '[ugly Lt. Littlepants]'], ['asspirate', '[indiscreet Sergeant Smallnuts]'], ['faggot', '[fudge baker]'], 
    ['tits', '[knockers]'], ['packer', '[baker]'], ['faggot', '[fudge baker]'], ['homo', '[interior decorator]'], ['cum', '[cream of sum yun guy]'], 
    ['fag', '[British cigarette]'], ['whore', '[corner warmer]'], ['spic ', '[spotted warbler]'], ['suck', '[bite]'], ['slut', '[ball warmer]'], 
    ['Disney', '[Di$ney]'], ['vagina', '[yeast infection]'], ['penis', '[man-meat]'], ['bitch', '[woman exhibiting symptoms of pre-menstrual syndrome]'],
    ['felcher', '[filter]'], ['newbie', '[nubile young thing]'], ['bastard', '[bar steward]'], ['piss ', '[pee-pee]'], ['douchebag', '[tampon]'], 
    ['fvck', '[fark]'], ['fcuk', '[French Connection United Kingdom]'], ['goddamn', '[Jesus loves me]'], ['breast', '[boobie]'], ['testicle', '[boobie]'],
    ['hell', '[New Jersey]'], ['orgy', '[party]'], ['dildo', '[chocolate covered double-dipped mocha ice cream with a cherry on top]'], 
    ['pimp', '[macdaddy]'], ['god damn', "[I'm a scientologist]"], ['nutlicker', '[Peter, peter pumpkin eater]'], 
    ['assmuncher', '[fat, fat fatty-fat]'], ['queer', '[Richard Simmons]'], ['homo', '[Tom Cruise]'], ['lesbo', '[gym teacher]'], 
    ['lezbo', '[senior citizen]'], ['lesbian', '[librarian]'], ['fish eater', '[vegetarian]'], ['bush', '[pubic region]'], ['clit', '[candy]'], 
    ['fuck you', '[I want to make sweet, sweet cyber love to you]']]
#lol long line of code right there :] 
#"my [phallic male genitalia of the penile organ genus] (now i'm just testing)" 
import re
def on_PRIVMSG(bot, sender, args):
    PREFIX = '!'
    nick, channel, args = sender.split('!', 1)[0], args[0], args[1]
    first = args
    
    if re.match(".*\[.*\].*",args):
        print "Needs unfiltering"
        for sub in table:
            if sub[1] in args:
                args = args.replace(sub[1],sub[0][0]+'.'+sub[0][1:])
    
        #print "Filter?"
#        print first
#        print args
    
    if first != args:
            bot.say(channel,args)
        



