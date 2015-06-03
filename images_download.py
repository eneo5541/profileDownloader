#!/usr/bin/python

import html.parser
import urllib.request

class PageParser(html.parser.HTMLParser):
	def handle_starttag(self, tag, attr):
		if tag.lower() == "a":
			for item in attr:
				if item[0].lower() == "href" and item[1].startswith("/view/"):
					links.append("http://www.test.net/full/"+item[1].split('/')[2]+"/")

class ImageParser(html.parser.HTMLParser):
	imgUrl = ""
	
	def handle_starttag(self, tag, attr):
		if tag.lower() == "a":
			self.imgUrl = attr[0][1]
	
	def handle_data(self, data):
		if (data.strip().lower() == "download"):
			fileName = self.imgUrl.split('/')[-1]
			if self.imgUrl.startswith("//"):
				self.imgUrl = "http:" + self.imgUrl
			urllib.request.urlretrieve(self.imgUrl, fileName)

def init():
	global targetPage
	targetPage = input('Page to download? (favorites/gallery)')
	if targetPage.lower() == "favourites":
		targetPage = "favorites"
	
	global targetUrl
	targetUrl = "http://www.test.net/" + targetPage + "/" + input('User page to download? ')
	
	confirm = input('Download contents of ' + targetUrl + "? (Y/N/abort)")
	if confirm.lower() == "y" or confirm.lower() == "yes":
		getPageLinks(targetUrl)
		parseLinks()
	elif confirm.lower() == "n" or confirm.lower() == "no":
		init()
	else:
		print("Aborting")

def getPageLinks(url):
	i = 1
	pageLinks = getLinks(url + "/" + str(i) + "/")
	prevLinks = 0
	print("Reading in ",len(links)," assets...")
	
	while len(links) > prevLinks:
		prevLinks = len(links)
		i += 1
		pageLinks = getLinks(url + "/" + str(i) + "/")
		print("Reading in ",len(links)," assets...")
	return

def getLinks( url ):
	request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	response = urllib.request.urlopen(request)
	html = response.read()
	
	parser = PageParser()
	parser.feed(str(html))
	return
	
def parseLinks():
	print("Total of ",len(links)," images...")
	
	for i in range(0, len(links)):
		print("Downloading ",i," of ",len(links),"...")
		request = urllib.request.Request(links[i], headers={'User-Agent': 'Mozilla/5.0'})
		response = urllib.request.urlopen(request)
		html = response.read()
		
		parser = ImageParser()
		parser.feed(str(html))
	
	print("Downloading completed")
	return

global links
links = []

init()