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
				
				fullfilename = os.path.join(destination, fileName)
				urllib.request.urlretrieve(imgUrl, fullfilename)

def init():
	global targetUrl
	targetUrl = "http://www.test.net/faves/" + input('User favourites to download? ')
	global destination
	destination = input('Destination for images? ')
	
	getFavouriteLinks(targetUrl)
	parseLinks()

def getFavouriteLinks( url ):
	i = 1
	pageLinks = getLinks(url + "/" + str(i) + "/")
	prevLinks = 0
	print("Reading in ",len(links)," assets...")
	
	# while len(links) > prevLinks:
		# prevLinks = len(links)
		# i += 1
		# pageLinks = getLinks(url + "/" + str(i) + "/")
		# print("Reading in ",len(links)," assets...")
	return

def getLinks( url ):
	request = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	response = urlopen(request)
	html = response.read()
	
	parser = FavouritePageParser()
	parser.feed(str(html))
	return
	
def parseLinks():
	print("Total of ",len(links)," images...")
	print(destination)
	for i in range(0, len(links)):
		print("Downloading ",i," of ",len(links),"...")
		request = Request(links[i], headers={'User-Agent': 'Mozilla/5.0'})
		response = urlopen(request)
		html = response.read()
		
		parser = ImagePageParser()
		parser.feed(str(html))
	
	print("Downloading completed")
	return


global links
links = []

init()