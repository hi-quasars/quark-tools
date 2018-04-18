import json
from common.common import *

class CheckEntry(object):
    def __init__(self, obj):
        self.ori     = obj['address']
        self.schema  = obj['schema']
        self.gMethod = obj['method']
        self.gAddr   = self.schema + self.ori
        self.gParams = {}
        # with check
        self.gParams['activity']  = obj['params']['activity']
        self.gParams['image_url'] = obj['params']['image_url']
        self.gOKFlag = obj['OKFlag']
        self.msg_if_err = self.settings('msg_if_err', obj['msg_if_err'])
        self.msg_if_ok  = self.settings('msg_if_ok', obj['msg_if_ok'])
        self.gSubTitle  = self.settings('subtitle', obj['subtitle'])

    def settings(self, whichset, type1 = 'default'):
        if whichset == 'msg_if_err':
            return 'Check service [' + self.ori + '] Failed'
        elif whichset == 'msg_if_ok':
            return 'Check service [' + self.ori + '] Success'
        elif whichset == 'subtitle':
            return self.ori
        else:
            return "not support"

    def init_from_json(self):
        pass
    def set_addr(self, addr1):
        self.ori_addr  = addr1
    def set_title(self, title1):
        self.gSubTitle = title1

class HttpCheck(object):
    def __init__(self):
        self.gEntries = []
        self.gEntries_attr = []
    def reinit_from_json(self, filename):
        self.gEntries = []
        jobject = od4file(filename, 'json')
        for et in jobject['allcheck']:
            e_name = et['name']
            e_conf = et['conf']
            etx = None
            try:
                etx = CheckEntry(e_conf)
            except Exception, e:
                return False,'init conf <' + e_name + '> failed: ' + str(e)
            if not etx is None:
                self.gEntries_attr.append({"name": e_name});
                self.gEntries.append(etx)
        return True, 'ok'
    def Show(self):
        for i in self.gEntries_attr:
            print i['name']

hc1 = HttpCheck()
hc1.reinit_from_json('./configs/CheckAlitiyu.conf')


if __name__ == "__main__":
    hc1 = HttpCheck()
    print hc1.reinit_from_json('./configs/CheckAlitiyu.conf')
    hc1.Show()
