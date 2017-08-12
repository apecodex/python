# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

headers = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36"}

r = requests.get("http://bangumi.bilibili.com/anime/3461",headers=headers)
b = BeautifulSoup(r.text,'lxml')
ber = b.find("ul",class_="slider-part clearfix hide").find_all("a")
html_tatal = []
for i in ber:
	title = i["href"]
	html_tatal.append(title)
	heads_name = i["title"]

html_url = requests.get(html_tatal[0],headers=headers)
html_soup = BeautifulSoup(html_url.text,"lxml")
html_find = html_soup.find("iframe",class_="player bilibiliHtml5Player")["src"]
print(html_find)