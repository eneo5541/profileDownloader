#!/usr/bin/python

from urllib.request import Request, urlopen
from html.parser import HTMLParser
import urllib.request
import os

class FavouritePageParser(HTMLParser):
	def handle_starttag(self, tag, attr):
		if tag.lower() == "a":
			for item in attr:
				if item[0].lower() == "href" and item[1].startswith("/view/"):
					links.append("http://www.test.net/full/"+item[1].split('/')[2]+"/")

class ImagePageParser(HTMLParser):
	def handle_starttag(self, tag, attr):
		if tag.lower() == "img":
			if attr[0][0] == "id" and attr[0][1] == "submissionImg" and attr[3][0] == "src":
				imgUrl = attr[3][1]
				fileName = imgUrl.split('/')[-1]
				if imgUrl.startswith("//"):
					imgUrl = "http:" + imgUrl
					
				path = "C:/Users/Eric/Desktop/images_script"
				fullfilename = os.path.join(path, fileName)
				urllib.request.urlretrieve(imgUrl, fullfilename)

def getFavouriteLinks( url ):
	i = 1
	pageLinks = getLinks(url + "/" + str(i) + "/")
	prevLinks = 0
	
	print("> ",len(links),"-",prevLinks)
	# while len(links) > prevLinks:
		# prevLinks = len(links)
		# i += 1
		# pageLinks = getLinks(url + "/" + str(i) + "/")
		# print(i," t ",len(links),"-",prevLinks);
	return

def getLinks( url ):
	request = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	response = urlopen(request)
	html = response.read()
	
	parser = FavouritePageParser()
	parser.feed(str(html))
	return
	
def parseLinks():
	if len(links) == 0:
		return
	
	request = Request(links[0], headers={'User-Agent': 'Mozilla/5.0'})
	response = urlopen(request)
	html = response.read()
	
	parser = ImagePageParser()
	parser.feed(str(html))
	return


global links
links = []
getFavouriteLinks('http://www.test.net/faves/test')
parseLinks()