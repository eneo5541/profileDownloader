#!/usr/bin/python

import html.parser
import urllib.request
import http.cookiejar
import urllib.parse
import re

from html.parser import HTMLParser
from html.entities import name2codepoint

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

class DL():
	view_link = '(http[s]?\:\/\/)?www\.test\.net\/view\/[0-9]+\/?'
	full_link = '(http[s]?\:\/\/)?www\.test\.net\/full\/[0-9]+\/?'
	cdn_link  = '(http[s]?\:\/\/)?d\.test\.net\/art\/.*(\.png|\.jpg|\.jpeg|\.gif)$'

	def __setup__(self):
		self.cookies = http.cookiejar.MozillaCookieJar('cookies-test.txt') #<-- Cookies
		try:
			self.cookies.load()
			print('Using stored cookie.')
			self.opener  = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cookies)) #<-- Cookie-aware url opener
			
			
			request = urllib.request.Request("http://www.test.net/faves/test/", headers={'User-Agent': 'Mozilla/5.0'})
			response = self.opener.open(request)
			html = response.read()
			
			parser = PageParser()
			parser.feed(str(html))
			print("Reading in ",len(links)," assets...")
			
			for i in range(0, len(links)):
				print("Downloading ",i," of ",len(links),"...")
				request = urllib.request.Request(links[i], headers={'User-Agent': 'Mozilla/5.0'})
				response = self.opener.open(request)
				html = response.read()
				
				parser = ImageParser()
				parser.feed(str(html))
			
		except http.cookiejar.LoadError as e:
			print('New login.')
			self.opener  = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cookies)) #<-- Cookie-aware url opener  
			self.__do_login__()

	def __do_login__(self):
		print ("Logging in as: %s pass: %s" % ('*'*len(self.user), '*'*len(self.passwd)) )
		#Login process
		self.opener.addheaders = [ ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:28.0) Gecko/20100101 Firefox/28.0') ]
		res = self.opener.open("https://www.test.net/login/") #<-- GET request, to get the cookies
		print("Getting login page. Status: %d" % res.status)
		if res.status != 200:
			raise "Couldn't get login page"
		headers = res.getheaders()
		for a,b in headers:
			if a == 'Set-Cookie':
				cookie = b
		#print("Set-Cookie: %s" % cookie) #<-- Redacted for production code
		res.read()

		#Prepare the login POST request
		params = urllib.parse.urlencode({'action': 'login', 'login': 'Login', 'name': self.user, 'pass': self.passwd})
		req = urllib.request.Request("https://www.test.net/login/", bytes(params, 'utf-8'))
		res = self.opener.open(req)

		print("Logging in. status: %d" % res.status)
		if res.geturl() == 'http://www.test.net/':
			print ("Login OK")
			res.read()
			self.cookies.save()
		else:
			res.read()
			raise "Failed to login"

	def __init__(self):
		self.user = "test_screenscraper"
		self.passwd = "302b2a2e40"
		self.__setup__()

	def is_link(self, url):
		if re.match(DL.view_link, url):
			return True
		elif re.match(DL.full_link, url):
			return True
		elif re.match(DL.cdn_link, url):
			return True

	def get_info(self, target):
		rv = {}
		if not self.is_link(target):
			return None
			
		if re.match(DL.cdn_link, target):
			rv['title'] = 'Link'
			rv['cdn'] = target
			rv['tags'] = []
			
			s = target
			s = s[:s.rfind('/')]
			s = s[s.rfind('/')+1:]
			rv['user'] = s
			rv['user-link'] = 'http://www.test.net/user/%s/' % s
			return rv
		else:
			page = self.get_decoded(target)
			cdn_parser = DLDownloadParser()
			cdn_parser.feed(page)
			rv['cdn'] = cdn_parser.get_download_link()
			if rv['cdn'] == None:
				return rv
				
			tag_parser = DLTagsParser()
			tag_parser.feed(page)
			rv['tags'] = tag_parser.get_tags()
			
			title_parser = DLTitleParser()
			title_parser.feed(page)
			rv['title'] = title_parser.get_title()
			
			s = rv['cdn']
			s = s[:s.rfind('/')]
			s = s[s.rfind('/')+1:]
			rv['user'] = s
			rv['user-link'] = 'http://www.test.net/user/%s/' % s
			return rv

def init():
	global targetPage
	targetPage = input('Page to download? (favorites/gallery)')
	if targetPage.lower() == "favourites":
		targetPage = "favorites"
	
	global targetUrl
	targetUrl = "http://www.test.net/" + targetPage + "/" + input('User page to download? ')
	
	confirm = input('Download contents of ' + targetUrl + "? (Y/N/abort)")
	if confirm.lower() == "y" or confirm.lower() == "yes":
		dl = DL()
		# getPageLinks(targetUrl)
		# parseLinks()
	elif confirm.lower() == "n" or confirm.lower() == "no":
		init()
	else:
		print("Aborting")
	# username = 'test_screenscraper'
	# password = '302b2a2e40'
	
def getPageLinks(url):
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