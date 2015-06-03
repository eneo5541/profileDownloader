#!/usr/bin/python

from urllib.request import Request, urlopen
from html.parser import HTMLParser
	
class FavouritePageParser(HTMLParser):
	def handle_starttag(self, tag, attr):
		if tag.lower() == "a":
			for item in attr:
				if item[0].lower() == "href" and item[1].startswith("/view/"):
					links.append("http://www.test.net/full/"+item[1].split('/')[2]+"/")

def init( url ):
	i = 1
	pageLinks = getLinks(url + "/" + str(i) + "/")
	prevLinks = 0
	print("> ",len(links),"-",prevLinks);
	while len(links) > prevLinks:
		prevLinks = len(links)
		i += 1
		pageLinks = getLinks(url + "/" + str(i) + "/")
		print(i," t ",len(links),"-",prevLinks);
	return

def getLinks( url ):
	request = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	response = urlopen(request)
	html = response.read()
	
	parser = FavouritePageParser()
	parser.feed(str(html))
	# print (html)
	return


global links
links = []
init('http://www.test.net/faves/test')