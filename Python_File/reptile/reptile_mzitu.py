# -*- coding: utf-8

import requests
from bs4 import BeautifulSoup

headers = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"}

url = "http://www.mzitu.com/all"
get_requests = requests.get(url,headers=headers)
get_beautifulsoup = BeautifulSoup(get_requests.text,"lxml")
get_soup = get_beautifulsoup.find("div",class_='all').find_all("a")

for i in get_soup:
	html_url = i["href"]
	html_requests = requests.get(html_url,headers=headers)
	html_Beautifulsoup = BeautifulSoup(html_requests.text,"lxml")
	html_soup = html_Beautifulsoup.find("div",class_="pagenavi").find_all("span")[-2].get_text()
	for page in range(1,int(html_soup)+1):
		page_url = html_url + "/" + str(page)
		page_requests = requests.get(page_url,headers=headers)
		page_BeautifulSoup = BeautifulSoup(page_requests.text,'lxml')
		page_soup = page_BeautifulSoup.find("div",class_="main-image").find("img")["src"]
		print(page_soup)