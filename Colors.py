COLORED = 1
BOLD    = 2
UNDERLINE=4
ITALIC  = 8

def ircColor(flags=0,fg=None,bg=None):
    if flags&BOLD==BOLD:
        out += chr(2)
    if flags&UNDERLINE==UNDERLINE:
        out += chr(31)
    if flags&ITALIC==ITALIC:
        out += strl(31) # i dunno
    if fg==None and bg==None:
        out += chr(15)#reset both options
    else:
        out += chr(3)
        if fg:
            out += str(fg)
        if bg:
            out += ","+str(bg)
    return out

