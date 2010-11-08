import traceback 
import sys
def printTrace():
	et, ev, tb = sys.exc_info()                                                 
	while tb :                                                                  
		co = tb.tb_frame.f_code                                                 
		filename = "Filename = " + str(co.co_filename)                          
		line_no =  "Error Line # = " + str(traceback.tb_lineno(tb))             
		print filename                                                          
		print line_no                                                           
		tb = tb.tb_next                                                         
	print "et = ", et                                                                    
	print "ev = ",  ev
	
def traceTest():
	try:
		print "1"
		print "0"
		print 1/0
	except:
		printTrace()

	