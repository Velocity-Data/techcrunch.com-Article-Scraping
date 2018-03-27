#!/usr/bin/env python
from bs4 import BeautifulSoup
import requests
import re
import os
import urllib
import subprocess
from requests.exceptions import ConnectionError
import time


links = [] 
log = []
txt = []
errors = ['ConnectionError... Retrying...', 'Url Timed-Out...']
date_time = time.ctime() 
excludes = ['You can also customize the types of stories it sends you.', 
	'TC Team', 'via,' 'You are about to activate', 
	'Facebook Messenger news bot' 'TC Messenger', 
	'Latest headlines delivered', 'Click on the button', 'photo:']


def Logger(inputtext, appendto, *extra):
	inp = date_time, inputtext
	if not extra:
		appendto.append(inp)
		print(inp)
	else:
		appendto.append(inp)
		appendto.append(extra)
		print(inp)

		
def getallLinks():
	yrpgs = ['2010/', '2011/', '2012/', '2013/', '2014/', '2015/', '2016/', '2017/', '2018/']
	mntpgs = ['01/', '02/', '03/', '04/', '05/', '06/', '07/', '08/', '09/', '10/', '11/', '12/']
	yrpgs = ['2010/', '2011/']
	mntpgs = ['01/', '02/']
	yrpgs.sort()
	mntpgs.sort()
	url = 'https://techcrunch.com/'
	url2 = ''
	url3 = ''
	links1 = []
	for a in yrpgs:
		url2 = url + a
		for b in mntpgs:
			url3 = url2 + b
			links1.append(url3)
	try:
		r = requests.get(url, timeout=60, allow_redirects=False)
		soup = BeautifulSoup(r.content, 'lxml')
		for link in soup.find_all('li', {'class': 'river-block'}):
			d = link.find('a')['href']
			if 'https://techcrunch.com/' in d:
				links.append(d)
				print(d)
	except requests.exceptions.Timeout:
		Logger(errors[1], log)
	ll = len(links), 'links have been found.'
	Logger(ll, log)

	
def scrape():
	try:
		for link in links:
			r = requests.get(link, timeout=60, allow_redirects=False)
			soup = BeautifulSoup(r.content, 'lxml')
			for i in soup.find_all('div', {'class': 'article-content'}):
				for j in soup.find_all('p'):
 					if any(ex in j.text for ex in excludes):
 						continue
 					else:
 						print(l.text)
 						txt.extend([l.text, ' '])
	except (ConnectionError, requests.exceptions.Timeout) as e:
		print(e)
		Logger(e, log)

		
def writetoFile(takefrom, writeto):
	txtfile = writeto +'.txt'
	txt1 = takefrom
	with open(txtfile, 'a') as f:
		for content in txt1:
			f.write(str(content))
	f.close()
	

if __name__ == '__main__':
	getallLinks()
	scrape()
	writetoFile(txt, 'article')
	ii = len(txt), 'Lines have been written to text file'
	Logger(ii, log)
	writetoFile(log, 'logfile')
