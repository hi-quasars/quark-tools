#
# BanyanDBTuner v0.2.0 -
#  TODO: example_conf ---> autogen
#

import json                        
from collections import OrderedDict
import os
import commands

#
# common
#
def wr2file(filename, ctn):
    with open(filename, "w") as f:
        f.write(ctn)

def rd4file(filename):
    with open(filename) as f:
        return f.read()

def od4str_pl(txt):
    ret = OrderedDict()
    conf = txt.split("\n")
    for l in conf:
        ss = l.split("=")
        if(len(ss) == 2):
            k = ss[0]
            v = ss[1]
            ret[k] = v
    return ret

def od2str_pl(od):
    str1 = ""
    for k, v in od.items():
        #print type(v)
        #assert type(v) == str
        str1 += "%s=%s\n" % (k, v)
    return str1

def od4file(filename, fm = "json"):
    txt = rd4file(filename)
    if fm == "json":
        return json.loads(txt, object_pairs_hook=OrderedDict)
    elif fm == "plain":
        return od4str_pl(txt)

def od2file(filename, od, fm = "json"):
    if fm == "json":
        wr2file(filename, json.dumps(od, indent = 4))
    elif fm == "plain":
        wr2file(filename, od2str_pl(od))

def val2list(way, li, val):
    if way == "push_back":
        li.insert(len(li), val)
    elif way == "push_front":
        li.insert(0, val)
    elif way == "pop_back":
        li.pop(len(li) - 1)
    elif way == "pop_front":
        li.pop(0)
    elif way == "clear":
		li[:] = []

def mkdir_if_miss(dirname):
    dirs = dirname.split("/")
    for i in range(1, len(dirs)):
		dirs[i] = dirs[i-1] + "/" + dirs[i]
    for i in dirs:
        if not os.path.exists(i):
            os.mkdir(i)

def run_bash_cmd(cmd):  #error handle
    os.system(cmd)

def run_bash_cmd_return_output(cmd):
    (status, output) = commands.getstatusoutput(cmd)
    return status, output

def remote_bash_cmd_return_output(cmd, user, host, port):
    if port == "":
        port = "22"
    bash = "ssh -p " + port + ' ' + user + '@' + host + ' \'' + cmd + '\''
    #print 'run: ' + bash
    (status, output) = commands.getstatusoutput(bash)
    #print 'status: ' + str(status)
    #print 'op: ' + output
    return status, output

import re
def md5sum_remote_file(user, host, port, remote_file_path):
    cmd = 'md5sum ' + remote_file_path;
    status, output = remote_bash_cmd_return_output(cmd, user, host, port)
    #print 'st:' + str(status)
    #print 'op:' + output
    op = output.split()
    if not status == 0:
        return None

    for i in range(len(op)):
        if op[i] == remote_file_path:
            return op[i-1]

def unzip_remote_file(user, host, port, remote_file_path, remote_dst_path):
    cmd = 'tar zxvf ' + remote_file_path + ' ' + '-C ' + remote_dst_path
    status, output = remote_bash_cmd_return_output(cmd, user, host, port)
    if status == 0:
        return remote_dst_path

def dir_zip(src, dst):
    if os.path.exists(src):
        bash = 'tar czvf ' + dst + ' -C ' + str_get_directory(src) + ' ' + str_get_file_name(src) + '/'
        #print "run: " + bash
        st, _ = run_bash_cmd_return_output(bash)
        if st == 0:
            return dst

def not_valid_str(str1):
    if str1 is None or str1 == "":
        return True
    return False

def str_get_file_name(str1):
    return str1.split('/')[-1]

def str_get_directory(str1):
    return '/'.join(str1.split('/')[:-1])

def cp_file_remote(user, host, port, local_dir, remote_dir_prefix):
    if port == "":
        port = "22"
    bash = 'scp -P ' + port + ' ' + local_dir + ' '+ user + '@' + host + ':' + remote_dir_prefix
    #print 'run: ' + bash
    (status, output) = run_bash_cmd_return_output(bash)
    #print 'status:' + str(status)
    #print 'op: ' + output
    return status, output

def md5sum(filename):
    bash = 'md5sum ' + filename
    (status, output) = run_bash_cmd_return_output(bash)
    if status == 0:
        return output.split(' ')[0]

def rm_dir(dirname):
    if os.path.exists(dirname):
        bash = 'rm -rf ' + dirname
        run_bash_cmd(bash)

def cp_dir(src, dst):
    if os.path.exists(src):
        bash = 'cp -r ' + src + ' ' + dst
        run_bash_cmd(bash)

def cp_dir_ctn(src, dst):
    if os.path.exists(src):
        bash = 'cp ' + src + '/* ' + dst
        run_bash_cmd(bash)

def cp_file(src, dst):
    if os.path.exists(src):
        bash = 'cp ' + src + ' ' + dst
        run_bash_cmd(bash)

def make_prefix(num, str1, li):
    prefix = [ str1 for i in range(num) ]
    prefix = "".join(prefix)
    ret = ""
    for i in li:
    	ret += "%s\n" % (prefix + i)
    return ret

def iport4str(str1):
    s1 = str1.split(":")
    return s1[0], s1[1]

import requests
def httpget(url, headers=None):
    s = requests.Session()
    try:
        res = s.get(url, headers = headers,stream=False)
    except Exception, e:
        return False, str(e)
    if res.status_code == 200:
        return True, res.content
    else:
        return False, res.status_code
