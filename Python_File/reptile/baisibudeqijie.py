# -*- condig: utf-8 -*-

import urllib.request
from bs4 import BeautifulSoup
import os


def video():
	os.mkdir("baisibudeqijie_video")
	time = 1
	while True:
		url = "http://www.budejie.com/video/"+str(time)
		time+=1
		headers = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36"}
		url_Request = urllib.request.Request(url,headers=headers)
		url_open = urllib.request.urlopen(url_Request)
		url_soup = BeautifulSoup(url_open.read().decode("utf-8"),'lxml')
		url_div = url_soup.find("li",class_="j-r-list-tool-l-down f-tar j-down-video j-down-hide ipad-hide").find_all("a")
		url_name = url_soup.find_all("li",class_="j-r-list-tool-l-down f-tar j-down-video j-down-hide ipad-hide")
		name = []
		div = []
		for i in url_name:
			name.append(i["data-text"])
		for x in url_div:
			div.append(x["href"])
		for z in zip(name,div):
			print("Downloading... %s" % z[0])
			urllib.request.urlretrieve(z[1],"baisibudeqijie_video//%s.mp4" % z[0])
			print("%s Download complite!" % z[0])

def img():
	os.mkdir("baisibudeqijie_img")
	time =1
	while True:
		url = "http://www.budejie.com/pic/"+str(time)
		time+=1
		headers = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36"}
		url_Request = urllib.request.Request(url,headers=headers)
		url_open = urllib.request.urlopen(url_Request)
		url_soup = BeautifulSoup(url_open.read().decode("utf-8"),'lxml')
		url_div = url_soup.find("div",class_="j-r-list-c-img").find_all("img")
		for i in url_div:
			title = i["title"]
			data_original = i["data-original"]
			img_Re = urllib.request.Request(data_original,headers=headers)
			img_open = urllib.request.urlopen(img_Re)
			print("Downloading... %s " % title)
			img_url = data_original.split(".")
			urllib.request.urlretrieve(data_original,"baisibudeqijie_img//%s" % (title+"."+img_url[-1]))
			print("%s Download complite!" % title)


print("--------------------------------")
print("| 1.video                      |")
print("| 2.img                        |")
print("--------------------------------")
user = input("请选择1 or 2: ")

if user == "1":
	print("正在获取页面...")
	video()
elif user == "2":
	print("正在获取页面...")
	img()
else:
	print("抱歉,选项里没有 '%s'" % user)