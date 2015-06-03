#!/usr/bin/python

from urllib.request import Request, urlopen
from html.parser import HTMLParser
	
class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attr):
        if tag.lower() == "a":
            for item in attr:
                if item[0].lower() == "href" and item[1].startswith("/view/"):
                    print(item[1])

def init( url ):
	i = 1
	pageLinks = getLinks(url + "/" + str(i) + "/")
	return
	
def getLinks( url ):
	request = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	response = urlopen(request)
	html = response.read()
	
	parser.feed(str(html))
	# print (html)
	return


parser = MyHTMLParser()
init('http://www.test.net/faves/test')