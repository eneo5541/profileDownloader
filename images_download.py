#!/usr/bin/python

import html.parser
import http.cookiejar
import urllib.request
import urllib.parse


class PageParser(html.parser.HTMLParser):
	def handle_starttag(self, tag, attr):
		if tag.lower() == "a":
			for item in attr:
				if item[0].lower() == "href" and item[1].startswith("/view/"):
					links.append("http://www.test.net/full/"+item[1].split('/')[2]+"/")


class ImageParser(html.parser.HTMLParser):
	imgUrl = ""
	def handle_starttag(self, tag, attr):
		if tag.lower() == "a" and len(attr) > 0 and len(attr[0]) > 1:
			self.imgUrl = attr[0][1]
	
	def handle_data(self, data):
		if (data.strip().lower() == "download"):
			fileName = self.imgUrl.split('/')[-1]
			if self.imgUrl.startswith("//"):
				self.imgUrl = "http:" + self.imgUrl
			urllib.request.urlretrieve(self.imgUrl, fileName)


class LoginHandler:		
	def requestLogin(self, cookies):
		opener.addheaders = [('User-Agent', 'Mozilla/5.0')]		
		params = urllib.parse.urlencode({'action': 'login', 'login': 'Login', 'name': 'test_screenscraper', 'pass': '302b2a2e40'})
		request = urllib.request.Request("https://www.test.net/login/", bytes(params, 'utf-8'))
		response = opener.open(request)
		
		if response.geturl() == 'http://www.test.net/':
			response.read()
			cookies.save()
		else:
			response.read()
			raise "Login failed"
	
	def __init__(self):
		print("Logging in...")
		
		global opener
		cookies = http.cookiejar.MozillaCookieJar('cookies-test.txt') #<-- Cookies
		try:
			cookies.load()
			opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookies)) #<-- Cookie-aware url opener	
		except http.cookiejar.LoadError as e:
			opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookies)) #<-- Cookie-aware url opener  
			self.requestLogin(cookies)
		
		print("Done.")

		
class ImageDownloader:
	def getLinks(self, url):
		request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
		response = opener.open(request)
		html = response.read()
		
		parser = PageParser()
		parser.feed(str(html))
	
	def getPageLinks(self, url):
		global links
		links = []
		i = 1
		pageLinks = self.getLinks(url + "/" + str(i) + "/")
		prevLinks = 0
		print("Reading in ",len(links)," assets...")
		
		while len(links) > prevLinks:
			prevLinks = len(links)
			i += 1
			pageLinks = self.getLinks(url + "/" + str(i) + "/")
			print("Reading in ",len(links)," assets...")
	
	def parseLinks(self):
		print("Total of ",len(links)," images...")
		
		for i in range(0, len(links)):
			print("Downloading ",i," of ",len(links),"...")
			request = urllib.request.Request(links[i], headers={'User-Agent': 'Mozilla/5.0'})
			response = opener.open(request)
			html = response.read()
			
			parser = ImageParser()
			parser.feed(str(html))
		
		print("Downloading completed")
	
	def __init__(self):
		global targetPage
		targetPage = input('Page to download? (favorites/gallery)')
		if targetPage.lower() == "favourites":
			targetPage = "favorites"
		
		global targetUrl
		targetUrl = "http://www.test.net/" + targetPage + "/" + input('User page to download? ')
		
		confirm = input('Download contents of ' + targetUrl + "? (Y/N/abort)")
		if confirm.lower() == "y" or confirm.lower() == "yes":
			login = LoginHandler()
			self.getPageLinks(targetUrl)
			self.parseLinks()
		elif confirm.lower() == "n" or confirm.lower() == "no":
			self.__init__()
		else:
			print("Aborting")


imageDownloader = ImageDownloader()