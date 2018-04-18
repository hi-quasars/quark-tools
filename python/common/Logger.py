import re
import datetime

LG_RED      = '\033[31m'
LG_YELLOW   = '\033[33m'
LG_GREEN    = '\033[32m'
LG_WHITE    = '\033[37m'
LG_END      = '\033[0m'


LG_ERROR    = 'Error'
LG_WARN     = 'Warnning'
LG_INFO     = 'Info'
LG_NORMAL   = 'Normal'

LG_INTERNALs = 10

LG_VERSION  = 0.01
#
# v0.1 Logger:
#   1. append write log file or clean & append write
#   2. log & print with color
# v0.2 -
#   1. add timestamp.

class LG(object):
    def __init__(self, filename = ".BanyanTuner.log", append = True):
        self.msg_type_prefix = {}
        self.msg_type_prefix[LG_ERROR]      = LG_RED        + '[ Error ] ' + LG_END
        self.msg_type_prefix[LG_WARN]       = LG_YELLOW     + '[ Warn  ] ' + LG_END
        self.msg_type_prefix[LG_INFO]       = LG_GREEN      + '[ Info  ] ' + LG_END
        self.msg_type_prefix[LG_NORMAL]     = LG_WHITE      + '[ Info  ] ' + LG_END
        
        self.lname  = filename 
        self.lobj   = open(self.lname, 'a') #append
        self.writeline("---- BanyanTuner Logger %s ----" % str(LG_VERSION))
	self.flush_internals = 0

    def __del__(self):
        self.lobj.close()
            
    def writeline(self, txt):
        self.lobj.write("%s\n" % txt)
    
    #type_a must be in `self.msg_type_prefix.keys()`
    def screen_str(self, type_a, txt): 
        return self.msg_type_prefix[type_a] + txt
        


    def Log(self, txt, type1 = '', screen = False):
        alltypes = [ i for i, j in self.msg_type_prefix.items() ];
        type1 = self.Type(type1)
        
        #date & time
        pref = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S  ')
        pref = '[' + pref + type1[0:3] + '] '
        txt = pref + txt

        if screen:
            print self.screen_str(type1, txt);

        self.writeline(txt)
        self.flush_internals = self.flush_internals + 1
	if (self.flush_internals > LG_INTERNALs):   
            self.lobj.flush();
            self.flush_internals = 0;

    def Type(self, txt):
        a1 = re.search('error|err', txt, re.I)
        a2 = re.search('warn|warning', txt, re.I)
        a3 = re.search('info|inf', txt, re.I)
        a4 = re.search('normal', txt, re.I)
        if txt == '':
            return LG_NORMAL

        if not a1 is None:
            return LG_ERROR
        elif not a2 is None:
            return LG_WARN
        elif not a3 is None:
            return LG_INFO
        elif not a4 is None:
            return LG_NORMAL

class Counter(object):
    def __init__(self):
        self.slist = None # stage list
        self.now_proc = 0 
        self.sum_proc = 0
        self.proc     = 0
    
    def setlist(self, li):
        self.slist = li
        self.now_proc = 0
        self.sum_proc = sum(self.slist)
        self.proc     = 0

    def clear(self):
        self.slist = None
        self.now_proc = 0
        self.sum_proc = 0
        self.proc     = 0

    def count(self):
        self.now_proc += 1
        p = self.now_proc * 1.0 / self.sum_proc * 100
        p = int(p) / 10
        if p > self.proc:
            self.proc = p
            return str(self.proc * 10)

