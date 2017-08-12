import urllib.request
from bs4 import BeautifulSoup
import os
import urllib.error

def Replace(url):
    url = url.replace("mvideo","svideo")
    url = url.replace("cn","com")
    url = url.replace("wpcco","wpd")
    return url

# os.mkdir("baisibudeqijie_peri")
# os.mkdir("baisibudeqijie_peri//baisibudeqijie_peri_img")
# os.mkdir("baisibudeqijie_peri//baisibudeqijie_peri_video")

def peri():
    time = 1
    while True:
        url = "http://www.budejie.com/tag/117/"+str(time)
        headers = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36"}
        url_Request = urllib.request.Request(url,headers=headers)
        try:
            url_open = urllib.request.urlopen(url_Request)
        except urllib.error.HTTPError as f:
            print("页面没有找到",f.code)
        url_soup = BeautifulSoup(url_open.read().decode("utf-8"),'lxml')
        try:
            url_img = url_soup.find("div",class_="j-r-c").find_all("img")
            url_video = url_soup.find("div",class_="j-r-c").find_all("div",class_=" j-video")
            url_video_name = url_soup.find_all("li",class_="j-r-list-tool-l-down f-tar j-down-video j-down-hide ipad-hide")
        except AttributeError as e:
            print("已经爬完了，这个网页的页面不多～不信自己翻一翻")

        img_link = []    # 图片的链接
        img_name = []    # 图片的名字
        video_link = []    # 视频的链接
        video_name = []    # 视频的名字
        video_name_split = []
        for i in url_video:
            video_link.append(Replace(i["data-mp4"]))
        for video_names in url_video_name:
            video_name.append(video_names["data-text"])
        for i in url_img:
            if "ugc" in i["data-original"]:
                img_name.append(i["alt"])
                img_link.append(i["data-original"])
        for i in video_name:
            video_name_split.append(i.split("，"))

        print("----------------------------------------")
        print("正在下载第 %s 页" % time)
        print("----------------------------------------")

        print("------------------------------------")
        print("开始下载视频...")
        for downloads in zip(video_name_split[0],video_link):
            try:
                print("Download... %s" % downloads[0])
                urllib.request.urlretrieve(downloads[1],"baisibudeqijie_peri//baisibudeqijie_peri_video//%s" % (downloads[0]+"."+downloads[1][-4:]))
                print("%s Download complite!" % downloads[0])
            except FileNotFoundError as e:
                print("视频链接没有找到，可能是被删除了吧～",e)
                pass
            if downloads[1] == video_link[-1]:
                continue
        print("视频已经下载完成...")
        print("------------------------------------")
        print("------------------------------------")
        print("开始下载图片....")
        for downloads in zip(video_name_split[0],video_link):
            try:
                print("Download... %s" % downloads[0])
                urllib.request.urlretrieve(downloads[1],"baisibudeqijie_peri//baisibudeqijie_peri_video//%s" % (downloads[0]+"."+downloads[1][-4:]))
                print("%s Download complite!" % downloads[0])
            except FileNotFoundError as e:
                print("视频链接没有找到，可能是被删除了吧～",e)
                pass
        print("图片已经下载完成...")
        print("---------------------------------")
        print("第 %s 页已经下载完成!" % time)

        time+=1

try:
    os.mkdir("baisibudeqijie_peri")
    os.mkdir("baisibudeqijie_peri//baisibudeqijie_peri_img")
    os.mkdir("baisibudeqijie_peri//baisibudeqijie_peri_video") 
    if os.path.exists("baisibudeqijie_peri_video"):
        os.rmdir("baisibudeqijie_peri//baisibudeqijie_peri_img")
        os.rmdir("baisibudeqijie_peri//baisibudeqijie_peri_video")
        os.rmdir("baisibudeqijie_peri")
        os.mkdir("baisibudeqijie_peri")
        os.mkdir("baisibudeqijie_peri_img")
        os.mkdir("baisibudeqijie_peri_video")
except FileExistsError:
    pass


peri()