import urllib2

def search(terms):
	terms = terms.replace(" ", "+")
	url = "http://www.citeulike.org/search/all?q=%s" % terms
	request = urllib2.Request(url)
	request.add_header('User-Agent', 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11')
	opener = urllib2.build_opener()
	data = opener.open(request).read()
	
	pairs = []
	
	for line in data.split("\n"):
		
		if '<a class="title"' in line:
			cols = line.split(">")
			title = cols[4][:-3]
			#print title
			#print cols[3]
			article_url = cols[3].split('="')[2][:-1]
			
			root = "http://www.citeulike.org/bibtex"
			end = "?do_username_prefix=0&key_type=0&incl_amazon=1&clean_urls=1&smart_wrap=1&q="
			
			bibtex_url = root + article_url + end
			pairs.append( (title, bibtex_url) )
			
			print '<a href="%s">%s</a>' % (bibtex_url, title)
	return pairs

def fetch_content( single_bibtex_url ):
	request = urllib2.Request(single_bibtex_url)
	request.add_header('User-Agent', 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11')
	opener = urllib2.build_opener()
	content = opener.open(request).read()
	return content

def append_content(comprehensive_file, content):
	f = open(comprehensive_file, "a")
	f.write("\n\n")
	f.write(content)
	f.close()


def append_bibtex(comprehensive_file, single_bibtex_url):
	content = fetch_content(single_bibtex_url)
	append_content(comprehensive_file, content)


#http://www.citeulike.org/bibtex/user/bigbossman/article/9038264?do_username_prefix=0&key_type=0&incl_amazon=1&clean_urls=1&smart_wrap=1&q=
#http://www.citeulike.org/bibtex/group/454/article/2399046?do_username_prefix=0&key_type=0&incl_amazon=1&clean_urls=1&smart_wrap=1&q=