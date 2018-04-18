import sys
sys.path.append('./common')
from Logger import LG
from common.common import *
import datetime
import time
import os

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


gPrefix = 'supervisor_'
gCheckInternal = 10          # 5s check internal
gSucceInternal = 360         # 360 1800/20=90 if ok, how many checks to send a email reporting ok. 0.5 hours


class log(object):
    def __init__(self, prefix = gPrefix, logdir = 'logs/'):
        self.prefix = prefix;
        self.logdir = logdir;
        self.ilog = None;
        # new log
        self.newlog(self.prefix, self.logdir);
        


    def newlog(self, prefix = gPrefix, logdir = 'logs/'):
        mkdir_if_miss(logdir);

        self.date1 = datetime.date.today()
        filename = logdir + prefix + str(self.date1) + '.log'       
        self.ilog = LG(filename)

    def doLog(self, txt, type1='info'):
        # check if a new log is needed
        today = datetime.date.today()
        if (today != self.date1):
            del self.ilog;
            self.newlog(self.prefix, self.logdir);
        
        self.ilog.Log(txt, type1, False);

from configs.mail import *

class Mail(object):
    def __init__(self, 
            mailuser = gMailUser, 
            who = gMailPrefix,
            password = gMailPassCode, 
            smtp_address = gSMTPAddr):
        self.smtpaddr = smtp_address
        self.mailuser = mailuser
        self.passwd = password
        self.maillist = [gToMailAddr]
        self.mestr = who + '<' + self.mailuser + '>'


    def Content(self, txt, sub):
        msg = MIMEText(txt, _subtype='plain', _charset='utf-8')
        msg['Subject'] = sub;
        msg['From'] = self.mestr;
        msg['To'] = self.ToList();
        return msg;

    def AddToMail(self, addr):
        self.maillist.append(addr);

    def ToList(self):
        return ';'.join(self.maillist)

    def Show():
        pass

    def Send(self, txt, sub):
        try:
            server = smtplib.SMTP()

            server.connect(self.smtpaddr);
            server.login(self.mailuser, self.passwd);

            ctn = self.Content(txt, sub);
            server.sendmail(self.mestr, self.ToList(), ctn.as_string())
            server.close()
        except Exception, e:
            return False, str(e)

        return True, "ok"

    def SendOK():
        pass
    def SendErr():
        pass

# check_routine
#  return True / False
#
#
DebugFlag = True
class Supervise:
    def __init__(self, check_routine, 
            name = 'default',
            internal_secs = gCheckInternal, 
            success_chks = gSucceInternal,
            arglist = None):
        self.routine    = check_routine
        self.internal   = internal_secs
        self.succsss_checks   = success_chks
        self.mail       = Mail()
        self.log        = log()
        self.check_routine = check_routine
        self.routine_args  = arglist
        self.succtimes  = 0
        self.chapter    = name

    def OKMsg(self):
        return self.chapter + ': check ok.'


    def Start(self):
        args_len = len(self.routine_args)
        rets = [False for i in self.routine_args]
        msgs = ["" for i in self.routine_args]

        while(1):
            time.sleep(self.internal)
            
            #send email
            if (self.succtimes > self.succsss_checks * args_len):
                for i in range(len(self.routine_args)):
                    ctx = self.routine_args[i]
                    title = self.chapter + '_' + ctx.gSubTitle
                    if(rets[i]):
                        self.log.doLog(self.chapter + ':' + 'send an OK email.');
                        self.mail.Send(self.chapter + ': OK, ' + msgs[i], 'OK:' + title[0:40]);
                self.succtimes = 0

            #check
            for i in range(len(self.routine_args)):
                ctx = self.routine_args[i]
                title = self.chapter + '_' + ctx.gSubTitle
                ret, msg1 = self.check_routine(ctx)
                rets[i] = ret
                msgs[i] = msg1
                if(ret == True):
                    self.succtimes = self.succtimes + 1
                    self.log.doLog('check ok - ' + title + msg1[53:95]);
                else:
                    self.log.doLog(self.chapter + ':' + 'check return false, ' + msg1, 'Err');
                    self.log.doLog(self.chapter + ':' + 'send an Err email.')
                    self.mail.Send(self.chapter + ': Error, ' + msg1,  'Failed:' + title[0:40]);
            
import requests
import json
def reqGet(url, data = None):
    response    = requests.get(url, params=data)
    res         = response.json()
    return res
def resCheck(json1, target1):
    keys1 = [k for k,v in json1.items() ]
    for k, v in target1.items():
        if k not in keys1:
            return False
        if json1[k] != v:
            return False
    return True


from HttpServiceCheck import *
def HttpBasedCheck(Ctx):
    confs = hc1.gEntries;
    if Ctx.gMethod == 'Get':
        try:
            res = reqGet(Ctx.gAddr, Ctx.gParams);
        except Exception, e:
            return False, Ctx.msg_if_err + ' - Get failed: ' + str(e)
        okflag = Ctx.gOKFlag;
        if resCheck(res, okflag):
            return True, Ctx.msg_if_ok + ' - ok, ' + str(res) + str(Ctx.gParams);
        return False, Ctx.msg_if_err + ' - Res Error: ' + str(res) + ', Params: ' + str(Ctx.gParams)

def AlitiyuCheck():
    entries = hc1.gEntries
    for i in entries:
        ret, msg1 = HttpBasedCheck(i)
        print ret, msg1


def func():
    tmpfile = './temp.txt'
    ret = os.path.exists(tmpfile)
    if not ret:
        return ret, tmpfile + 'not exist.'
    return ret, 'ok'

def test_mail():
    email = Mail()
    ret, msg = email.Send('Test Message', 'Test Subject')
    if (ret):
        print "ok"


def runx(func1, arglist):
    for i in arglist:
        ret, msg = func1(i)
        print 'err: ' + msg

def funcheck(arg):
    if arg == 'yes':
        return True, 'ok'
    return False, 'notxxx'

def test_func_as_arg():
    runx(funcheck, ['yes', '111'])

def test_main():
    s1 = Supervise(HttpBasedCheck, 'AlitiyuCheck', arglist = hc1.gEntries);
    s1.Start()


if __name__ == "__main__":
    test_main()
