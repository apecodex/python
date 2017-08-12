# -*- coding: utf-8 -*-

import urllib.request
from bs4 import BeautifulSoup

url = "https://www.dou-bi.co/sszhfx/"
headers = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36"}
url_RE = urllib.request.Request(url,headers=headers)
url_open = urllib.request.urlopen(url_RE)
url_soup = BeautifulSoup(url_open.read().decode("utf-8"),"lxml")
url_lxml = url_soup.find("div",class_="article-content").find_all("td")
for i in url_lxml:
	print(i)