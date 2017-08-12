# -*- coding: utf-8 -*-

import urllib.request
import urllib.error
from bs4 import BeautifulSoup
import os

headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36"}

url = "http://www.qiushibaike.com/"
url_Re = urllib.request.Request(url,headers=headers)
url_open = urllib.request.urlopen(url_Re)
url_soup = BeautifulSoup(url_open.read().decode("utf-8"),'lxml')
url_find_text = url_soup.find("div",class_="col1").find_all("div",class_="content")
url_find_img = url_soup.find("div",class_="col1").find_all("img")
url_img = []
url_name = []
url_text = []
url_text_name = []
print("------------------------")
print("正在下载图片")
for i in url_find_img:
    if "pictures" in i["src"]:
        url_img.append(i["src"])
        url_name.append(i["alt"])

for text in url_find_text:
    url_text.append(text.get_text())
for name in url_text:
    url_text_name.append(name.replace("\n", ""))
print(url_text_name)
"""
for img in zip(url_name,url_img):
    try:
        print("------------------------")
        print("Downdload... %s" %img[0])
        urllib.request.urlretrieve(img[1],img[0]+img[1][-5:])
        print("%s Download Complite!" % img[0])
    except FileNotFoundError as e:
        print("链接消失或者目录没创建",e)
    if img[1] == url_img[-1]:
        continue
print("------------------------")
print("图片已经下载完成")
"""


print("------------------------")
print("正在开始下载段子")


def Heat_map():
    time = 1
    while True:
        url = "http://www.qiushibaike.com/imgrank/page/"+str(time)+"/?s=4942216"
        try:
            url_Re = urllib.request.Request(url,headers=headers)
            url_open = urllib.request.urlopen(url_Re)
            url_soup = BeautifulSoup(url_open.read().decode("utf-8"),"lxml")
            url_find = url_soup.find("div",class_="col1").find_all("img")
        except urllib.error.HTTPError as e:
            print("链接没有找到",e.code)
        except AttributeError as a:
            print("已经爬完了，页面并不多，不信自己翻一翻~",a)
            break
        print("---------------------------------")
        print("正在下载第 %s 页" % time)
        for i in url_find:
            if "pictures" in i["src"]:
                try:
                    print("Download... %s" % i["alt"])
                    urllib.request.urlretrieve(i["src"],"img//%s"%(i["alt"]+i["src"][-5:]))
                    print("%s Download Complite!" % i["alt"])
                except FileNotFoundError as f:
                    print("链接消失了或者目录没创建~",f)
        print("第 %s 页已经下载完成!" % time)
        print("---------------------------------")
        time+=1
