# -*- condig: utf-8 -*-

import urllib.request
from bs4 import BeautifulSoup
import os
import urllib.error

def Replace(url):
    url = url.replace("mvideo","svideo")
    url = url.replace("cn","com")
    url = url.replace("wpcco","wpd")
    return url

def video():
    time = 1
    while True:
        url = "http://www.budejie.com/video/"+str(time)
        headers = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36"}
        url_Request = urllib.request.Request(url,headers=headers)
        try:
            url_open = urllib.request.urlopen(url_Request)
        except urllib.error.HTTPError as e:
            print("页面没有找到",e.code)
        url_soup = BeautifulSoup(url_open.read().decode("utf-8"),'lxml')
        try:
            url_div = url_soup.find("div",class_="j-r-c").find_all("div",class_=" j-video")
            url_name = url_soup.find_all("li",class_="j-r-list-tool-l-down f-tar j-down-video j-down-hide ipad-hide")
        except AttributeError as f:
            print("已经爬完了...这个网站页面不多~不信自己翻一翻")
            break
        name = []  #用来储存视频的名字
        div = []   # 用来储存视频的地址
        replace_name = []   # 将视频名字中的一些特殊字符换掉
        for i in url_name:
            name.append(i["data-text"])
        for z in name:
            z = z.replace("\"","'")
            replace_name.append(z)
        for x in url_div:
            video_url =  Replace(x["data-mp4"])
            div.append(video_url)
        print("------------------------------------")
        print("正在下载第 %s 页" % time)
        for z in zip(replace_name,div):
            print("Downloading... %s" % z[0])
            urllib.request.urlretrieve(z[1],"baisibudeqijie_video//%s.mp4" % z[0])
            print("%s Download complite!" % z[0])
        print("第 %s 页已下载完成" % time)
        print("------------------------------------")
        time+=1

def img():
    time = 1
    while True:
        url = "http://www.budejie.com/pic/"+str(time)
        headers = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36"}
        url_Request = urllib.request.Request(url,headers=headers)
        try:
            url_open = urllib.request.urlopen(url_Request)
        except urllib.error.HTTPError as f:
            print("页面没有找到",f.code)
        url_soup = BeautifulSoup(url_open.read().decode("utf-8"),'lxml')
        try:
            url_div = url_soup.find("div",class_="j-r-list").find_all("img")
        except AttributeError as e:
            print("已经爬完了，这个网页的页面不多～不信自己翻一翻")
        url_img = []   # 图片的地址
        url_name = []   # 图片的名字
        for i in url_div:
            url_img.append(i["data-original"])
            url_name.append(i["alt"])
        url_reght = []  # 这个网站的图片会有一些不是图片的链接出现，没有后缀的~下载下来也没用，把它去掉
        a = [".gif",".png",".jpg"]
        for i in url_img:
            if i[-4:] in a:
                url_reght.append(i)
        url_name_split = []  # 因为字符串太长，储存的时候会报错，就截取'，'前面第一个
        for name_split in url_name:
            url_name_split.append(name_split.split("，"))
        print("--------------------------------")
        print("正在下载第 %s 页" % time)
        for download in zip(url_name_split,url_reght):
            img_Re = urllib.request.Request(download[1],headers=headers)
            img_open = urllib.request.urlopen(img_Re)
            print("Download... %s" % download[0][0])
            urllib.request.urlretrieve(download[1],"baisibudeqijie_img//%s" % (download[0][0]+"."+download[1][-4:]))
            print("%s download complite!" % download[0][0])
        print("第 %s 页已经下载完成" % time)
        time+=1

def text():
    time = 1
    while True:
        url = "http://www.budejie.com/text/"+str(time)
        headers = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36"}
        url_Request = urllib.request.Request(url,headers=headers)
        try:
            url_open = urllib.request.urlopen(url_Request)
        except urllib.error.HTTPError as f:
            print("页面没有找到",f.code)
        url_soup = BeautifulSoup(url_open.read().decode("utf-8"),'lxml')
        try:
            url_text = url_soup.find("div",class_="j-r-c").find_all("div",class_="j-r-list-c-desc")
            url_name = url_soup.find("div",class_="j-r-c").find_all("div",class_="u-txt")
        except AttributeError as e:
            print("已经爬完了，这个网页的页面不多～不信自己翻一翻")
        text = []  # 段子
        name = []  # 发送人的用户名
        name_split= []  # 用户名的格式是用户名+时间，把它两个分开
        for x in url_name:
            name.append(x.get_text())
        for i in url_text:
            text.append(i.get_text())
        for name_splits in name:
            splits = name_splits.split(" ")
            name_split.append(splits)
        print("-------------------------------")
        print("正在下载第 %s 页" % time)
        for download in zip(name_split,text):
            print("Download... %s" % download[0][0])
            with open("baisibudeqijie_text//%s" % (download[0][0]+download[0][1]+download[0][2]+".txt"),"w") as f:
                f.write(download[1])
            print("%s Download complite" % download[0][0])
        print("第 %s 页已经下载完成" % time)
        print("-------------------------------")
        time+=1


print("--------------------------------")
print("| 1.video                      |")
print("| 2.img                        |")
print("| 3.text                       |")
print("--------------------------------")
user = input("请选择1 or 2: ")

if user == "1":
    print("正在获取页面...")
    try:
        os.mkdir("baisibudeqijie_video")              # 这里就是先创建，如果存在就删除，然后重新创建
        if os.path.exists("baisibudeqijie_video"):
            os.rmdir("baisibudeqijie_video")
            os.mkdir("baisibudeqijie_video")
    except FileExistsError:
        pass
    video()
elif user == "2":
    print("正在获取页面...")
    try:
        os.mkdir("baisibudeqijie_img")
        if os.path.exists("baisibudeqijie_img"):
            os.rmdir("baisibudeqijie_img")
            os.mkdir("baisibudeqijie_img")
    except FileExistsError:
        pass
    img()
elif user == "3":
    print("正在获取页面...")
    try:
        os.mkdir("baisibudeqijie_text")
        if os.path.exists("baisibudeqijie_text"):
            os.rmdir("baisibudeqijie_text")
            os.mkdir("baisibudeqijie_text")
    except FileExistsError:
        pass
    text()
else:
    print("抱歉,选项里没有 '%s'" % user)
