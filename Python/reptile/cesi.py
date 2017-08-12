# -*- coding: utf-8 -*-


import urllib.request
from bs4 import BeautifulSoup
import os
import urllib.error
os.mkdir("baisibudeqijie_audio")
def audio():
	time = 1
	while True:
		url = "http://www.budejie.com/audio/"+str(time)
		headers = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36"}
		url_Request = urllib.request.Request(url,headers=headers)
		try:
			url_open = urllib.request.urlopen(url_Request)
		except urllib.error.HTTPError as f:
			print("页面没有找到",f.code)
		url_soup = BeautifulSoup(url_open.read().decode("utf-8"),'lxml')
		try:
			url_audio = url_soup.find("div",class_="j-r-c").find_all("div",class_=" j-audio")
			url_name = url_soup.find("div",class_="j-r-c").find_all("div",class_="j-r-list-c-desc")
		except AttributeError as e:
			print("已经爬完了，这个网页的页面不多～不信自己翻一翻")

		audio_link = []   # audio的链接
		audio_name = []   # audio的名字
		audio_split = []    # 名字太长会报错，分开
		audio_relpace_n = []    # 有'\n'会报错，换掉
		audio_relpace_r = []    # 有'\r'也会报错，换掉

		for x in url_audio:
			audio_link.append(x["data-mp3"])

		for i in url_name:
			audio_name.append(i.get_text().replace(" ",""))

		for i in audio_name:
			audio_split.append(i.split("，"))

		for n in audio_split:
			audio_relpace_n.append((n[0].replace("\n","")))
		for r in  audio_relpace_n:
			audio_relpace_r.append(r.replace("\r",""))
		print("--------------------------------------")
		print("正在下载第 %s 页" % time)
		for download in zip(audio_relpace_r,audio_link):
			try:
			    print("Download... %s" % download[0])
			    urllib.request.urlretrieve(download[1],"baisibudeqijie_audio//%s" % (download[0]+".mp3"))
			    print("%s Download complite!" % download[0])
			except FileNotFoundError as e:
				print("没有找到,可能是被删除了吧～",e)
				pass
		print("第 %s 页已经下载完成！" % time)
		print("--------------------------------------")
		time+=1
audio()