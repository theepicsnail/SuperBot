
#!/usr/bin/python
# 1,2,(3,4)
# [1,[2,[(3,4)]]
#
#x =
#x = 1-2-3-4-5
#2^3^4
#2^3^4+5
#symbols val
#  =     4  <- split if you ever see this 
#  ,     4  set if val < 4
#  +-    3  set if val <= 3
#  */    2  set if val <= 2
#  ^     1  set if val <  1

IMPORT_MATH=True

funcs={}
globalVars={}

_int = int
_float = float
_complex = complex
_smartint=lambda x:int(float(x))
convert = _float


def args(line):
   a = line.split(",")
   return map(lambda x:[x,"Var"] if len(x)==0 or x.startswith("#") else [Exception("Expected variable, found %s"%x)],a)
def primOrFunc(line):
   try: #if it's a number (more than likely) try to convert it 
      return [convert(line),"Prim"]
   except:
      pass
   
   if(line.endswith(")")):# if it ends with a ) it's probably a 'func(expr)'
      parts = line[:-1].split("(",1)
      return [parts[0],'Call',parse(parts[1])]
   #else it's a number that failed to convert, or it's a variable
   if line.startswith("#"):
      return [line,"Var"]
   return Exception("Expected number/function/variable, but found:'%s'."%line)

def LHS(line):
   if(line.endswith(")")):# if it ends with a ) it's probably a 'name(#a,#b)'
      parts = line[:-1].split("(",1)
      return [parts[0],'Call',args(parts[1])]
   #else it's a number that failed to convert, or it's a variable
   if line.startswith("#"):
      return [line,"Var"]
   return Exception("Expected number/function/variable, but found:'%s'."%line)

def parse(line):
   print line
   marker = [0,-1]#pos val
   parenLevel = 0
   inParens = True
   lastOpeningParen = -1
   for i in range(len(line)):
      if line[i]==')':
         parenLevel-=1
         if parenLevel <0:
            return [Exception("Extra )",i)]
         continue
      elif line[i]=='(':
         lastOpeningParen = i
         parenLevel+=1   
         if inParens and parenLevel==0:
            inParens= (i==0)
         continue
      if parenLevel==0:
         inParens = False
         if line[i] == '=': 
            parts = line.split('=',1)
            return [LHS(parts[0]),'=',parse(parts[1])]
         if (line[i] == ',') and marker[1] < 4:
            marker[0] = i
            marker[1] = 4
         if (line[i] == '-' or line[i]=='+') and marker[1] <= 3:
            marker[0] = i
            marker[1] = 3
         if (line[i] == '/' or line[i]=='*') and marker[1] <= 2:
            marker[0] = i
            marker[1] = 2
         if (line[i] == '^') and marker[1] < 1:
            marker[0] = i
            marker[1] = 1
   if parenLevel!=0:
      return [Exception("Unclosed (",lastOpeningParen)]
   if inParens:
        return parse(line[1:-1]) 
   else:
      if marker[1]==-1:
         return primOrFunc(line)
      parts = line[:marker[0]],line[marker[0]+1:]
      if line[marker[0]]=='-' and parts[0]=="":
         return [None,"-",parse(parts[1])]
      return [parse(parts[0]),line[marker[0]],parse(parts[1])]

def checkErrors(tree):
   foundError = False
   if type(tree) == list:
      for i in tree:
         r = checkErrors(i)
         if r:
            return r
   elif type(tree)==Exception:
      return tree
   return False



def setVar(varSpace,name,val):
   varSpace[name[0]]=val
   return val
def setFunc(name,arglist,tree):
   funcs[name]=[tree,arglist]
def lookupVar(varSpace,name):
   if varSpace.has_key(name):
      return varSpace[name]
   return 0

      #argcount  0 = takes a list, 
def addBuiltinFunction(name,func,argcount):
   if argcount!=0:
      argNames = []
      for i in range(argcount):
         argNames+=["#param%i"%i]
         setFunc(name,argNames,lambda x,y:func(*x))
   else:
      setFunc(name,["#params"],lambda x,y:func(*x))


def addBuiltinVar(name,val):
   setVar(globalVars,[name,"Var"],val)
def lookupFunc(name):#[functionExpr, functionArgs]
   if funcs.has_key(name):
      return funcs[name]
   return Exception("Function %s not found."%name)


def evaluate(tree,varSpace):
   print tree,varSpace
   #most recursions will be using the same varspace
   ev = lambda x:evaluate(x,varSpace)

   if tree[1]=="=":
      lhs = tree[0]
      if lhs[1]=="Var":
         return setVar(varSpace,lhs,ev(tree[2]))
      if lhs[1]=="Call":
         return setFunc(lhs[0],lhs[2],tree[2])
   elif tree[1]=="+":
      return ev(tree[0])+ev(tree[2])
   elif tree[1]=="-":
      if tree[0]:
         return ev(tree[0])-ev(tree[2])
      return -1 * ev(tree[2])
   elif tree[1]=="*":
      return ev(tree[0])*ev(tree[2])
   elif tree[1]=="/":
      return ev(tree[0])/ev(tree[2])
   elif tree[1]=="^":
      return ev(tree[0])**ev(tree[2])
   elif tree[1]=="Var":
      return lookupVar(varSpace,tree[0])
   elif tree[1]=="Prim":
      return tree[0]
   elif tree[1]==",":
      out = ev(tree[2])
      base = [ev(tree[0])]
      if type(out)==list:
         return base+out
      return base+[out]
   elif tree[1]=="Call":
#      print "-"*30
      f=lookupFunc(tree[0])
 #     print "f:",f
      if type(f)==Exception:
         raise Exception("Unknown function '%s'"%tree[0])
      t = ev(tree[2])
  #    print "t:",t
      if type(t)!=list:
         t=[t]
      vs = varSpace.copy()
      for i in range(len(f[1])):
         vs[f[1][i][0] ]=t[i]
   #   print "vs:",vs
      if callable(f[0]):
         return f[0](t,vs)
      return evaluate(f[0],vs)
   
if IMPORT_MATH:
   import math
   addBuiltinFunction("acos",math.acos,1)
   addBuiltinFunction("acosh",math.acosh,1)
   addBuiltinFunction("asin",math.asin,1)
   addBuiltinFunction("asinh",math.asinh,1)
   addBuiltinFunction("atan",math.atan,1)
   addBuiltinFunction("atan2",math.atan2,2)
   addBuiltinFunction("atanh",math.atanh,1)
   addBuiltinFunction("ceil",math.ceil,1)
   addBuiltinFunction("copysign",math.copysign,2)
   addBuiltinFunction("cos",math.cos,1)
   addBuiltinFunction("cosh",math.cosh,1)
   addBuiltinFunction("degrees",math.degrees,1)
   addBuiltinFunction("exp",math.exp,1)
   addBuiltinFunction("fabs",math.fabs,1)
   addBuiltinFunction("factorial",math.factorial,1)
   addBuiltinFunction("floor",math.floor,1)
   addBuiltinFunction("fmod",math.fmod,1)
   addBuiltinFunction("frexp",math.frexp,1)
   addBuiltinFunction("fsum",math.fsum,0)
   addBuiltinFunction("hypot",math.hypot,2)
   addBuiltinFunction("isinf",math.isinf,1)
   addBuiltinFunction("isnan",math.isnan,1)
   addBuiltinFunction("ldexp",math.ldexp,1)
   addBuiltinFunction("log",math.log,1)
   addBuiltinFunction("log10",math.log10,1)
   addBuiltinFunction("log1p",math.log1p,1)
   addBuiltinFunction("modf",math.modf,1)
   addBuiltinFunction("pow",math.pow,2)
   addBuiltinFunction("powmod",math.pow,3)
   addBuiltinFunction("radians",math.radians,1)
   addBuiltinFunction("sin",math.sin,1)
   addBuiltinFunction("sinh",math.sinh,1)
   addBuiltinFunction("sqrt",math.sqrt,1)
   addBuiltinFunction("tan",math.tan,1)
   addBuiltinFunction("tanh",math.tanh,1)
   addBuiltinFunction("trunc",math.trunc,1)
   addBuiltinVar("#pi",math.pi)
   addBuiltinVar("#e",math.e)
def makeFunc(name):
    def onBind(func):
        addBuiltinFunction(name,func,func.func_code.co_argcount)
    return onBind

@makeFunc("if")
def _if(a,b,c):
    return b if a else c

@makeFunc("gt")
def gt(x,y): return 1 if x>y else 0

@makeFunc("lt")
def lt(x,y): return 1 if x<y else 0

@makeFunc("max")
def m(*x):
    max = x[0]
    for i in x:
        if i>max:
            max = i
    return max
@makeFunc("index")
def idx(a,*b):
    return b[int(a)]


import sys
verbose = False
def handleLine(line):
   global verbose,convert
   options=line.split(":")
   for i in range(len(options)-1):
      for j in options[i]:
         if j=='s':
            convert=_smartint
         if j=='f':
            convert=_float
         if j=='i':
            convert=_int
         if j=='c':
            convert=_complex
         if j=='v':
            verbose=True
   x = parse(options[-1])
   err = checkErrors(x)
   if err and verbose:
      return err
   else:
      try:
         return setVar(globalVars,"#",evaluate(x,globalVars))
      except Exception, e:  
         if verbose:
            return e
         pass



def on_load(bot):
    bot.noticeCount = 0

def on_unload(bot):
    print "unloaded"

def on_NOTICE(bot,nickLine,params):
    print bot.noticeCount
    bot.noticeCount+=1

def on_PRIVMSG(bot,sender,args):
    print sender,args
    line = args[1]
    if line.startswith("%"):
        line=line[1:]
        out = handleLine(line)
        print "Say:",sender[0],out
        bot.say(args[0],str(out))
        
