import urllib,urllib2
import cookielib
import string

URLMain 	= 'http://bbs.xmfish.com'
URLLogin 	= 'http://www.xiaoyu.com/login'
URLphp		= 'http://bbs.xmfish.com/u.php'
def_post_header = {
#	'':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#	'':'gzip, deflate',
#	'':'en-US,en;q=0.5',
#	'':'',
#	'':'',
#	'':'',
	'Referer':'http://bbs.xmfish.com/u.php?jumpurl=http%3A%2F%2Fbbs.xmfish.com%2Fu.php%3Fjumpurl%3Dhttp%3A%2F%2Fbbs.xmfish.com%2Fu.php%3Fjumpurl%3Dhttp%3A%2F%2Fbbs.xmfish.com%2Fu.php%3Fjumpurl%3Dhttp%3A%2F%2Fbbs.xmfish.com%2Fu.php',
#	'User-Agent':''
}
def_post_data = {
'jumpurl':'http://bbs.xmfish.com/u.php?jumpurl=http://bbs.xmfish.com/u.php?jumpurl=http://bbs.xmfish.com/u.php?jumpurl=http://bbs.xmfish.com/u.php?jumpurl=http://bbs.xmfish.com/u.php',
'loginurl':'http://bbs.xmfish.com/u.php',
'action':'bbs',
'bbs_id':'63',
'username':'your_id',
'password':'your_passwd'
}


def cookie_generator():
	cookie = cookielib.CookieJar()
	handler = urllib2.HTTPCookieProcessor(cookie)
	opener = urllib2.build_opener(handler)
	opener.open(URLLogin)
	return cookie, opener 
def cookie_print(ck):
	print "| %-20s | %-30s |" % ( "name", "value")
	for item in ck:
		print "| %-20s | %-30s |" % (item.name, item.value)
def post_header():
	pass

def make_req(op):
	data = urllib.urlencode(def_post_data)
	req = urllib2.Request(URLLogin, data = data, headers = def_post_header)
	resp = op.open(req)
	return resp

def find_urls(text):
	lines = text.split('\n')
	settingurls = []
	settingurls_hit = False;
	for i in range(len(lines)):
		if ('script type="text/javascript"' in lines[i]) and ('ready(function()' in lines[i + 1]):
			settingurls_hit = True
			#print 'true'
			
		if '</script>' in lines[i]:
			settingurls_hit = False
			#print 'false'
		
		if settingurls_hit :
			raw = lines[i]
			if 'url' in raw:
				st = string.find(raw,'\'')
				ed = string.find(raw[st+1:],'\'')	
				#print raw[st+1 : ed + st + 1]
				settingurls.append(raw[st+1 : ed + st + 1])
	
		if 'setTimeout' in lines[i]:
			raw = lines[i+1]
			st = string.find(raw,'\'')
			ed = string.find(raw[st+1:],'\'')
			finalurl = raw[st+1 : ed + st + 1]
	
	return settingurls, finalurl
	
	
def get_page(op, url):
	resp = op.open(url)
	return resp
	
if __name__ == "__main__":
	ck, fd = cookie_generator()
	cookie_print(ck)
	print "======================="
	resp = make_req(fd)
	text = resp.read()
	with open("jumping.html", "w") as f:
		f.write(text)

	urlist, furl = find_urls(text)
	idx = 0
	for i in urlist:
		print "----------%d----------" % idx
		resp = get_page(fd, i)
		print(resp.read())
		idx = idx + 1
		
	resp = get_page(fd, furl)
	with open("final.html", "w") as f:
		f.write(resp.read())
	
