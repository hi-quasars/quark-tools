import string

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

with open("jumping.html", "r") as f:
	text = f.read()
	find_urls(text)