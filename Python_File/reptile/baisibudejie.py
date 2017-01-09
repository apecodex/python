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
            try:
                print("Downloading... %s" % z[0])
                try:
                    urllib.request.urlretrieve(z[1],"baisibudeqijie_video//%s.mp4" % z[0])
                    print("%s Download complite!" % z[0])
                except OSError as o:
                    print("文件出错啦~可能是有特殊符号~也有可能是链接消失啦~这张就下载不了啦~",o)
            except UnicodeEncodeError as u:
                print("你用的可能是windows系统吧~这里报错“GBK”了~用Linux系统吧~")
                print("或者在cmd窗口下输入: chcp 65001 就可以改成'utf-8'了")
            except urllib.error.HTTPError as f:
                print("图片链接没有找到,可能是被删除了吧～",f.code)
            except FileNotFoundError as e:
                print("视频链接没有找到,可能被删除了吧～",e)
                pass
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
            url_div = url_soup.find("div",class_="j-r-c").find_all("img")
            url_name = url_soup.find("div",class_="j-r-c").find_all("div",class_="j-r-list-c-desc")
        except AttributeError as e:
            print("已经爬完了，这个网页的页面不多～不信自己翻一翻")
        url_img = []   # 图片的地址
        img_name = []   # 图片的名字
        img_link = []   # 图片地址有错误的链接~筛选掉
        img_name_replace = []  # 名字有"\n"得去掉
        a = [".gif",".png",".jpg"]
        for i in url_div:
            if i["data-original"][-4:] in a:
                url_img.append(i["data-original"])
        for i in url_img:
            if i.split("/")[3] != "profile":
                img_link.append(i)
        for i in url_name:
            img_name.append(i.get_text())
        for x in img_name:
            img_name_replace.append(x.replace("\n",""))
        print("------------------------------------")
        print("正在下载第 %s 页" % time)
        for download in zip(img_name_replace,img_link):
            try:
                print("Download... %s" % download[0])
                try:
                    urllib.request.urlretrieve(download[1],"baisibudeqijie_img//%s" % (download[0][0:20]+download[1][-5:]))
                except OSError as o:
                    print("文件出错啦~可能是有特殊符号~也有可能是链接消失啦~这张就下载不了啦~",o)
                print("%s download complite!" % download[0])
            except UnicodeEncodeError as u:
                print("你用的可能是windows系统吧~这里报错“GBK”了~用Linux系统吧~")
                print("或者在cmd窗口下输入: chcp 65001 就可以改成'utf-8'了")
            except urllib.error.HTTPError as f:
                print("图片链接没有找到,可能是被删除了吧～",f.code)
            except FileNotFoundError as e:
                print("图片链接没有找到,可能是被删除了吧～",e)
                pass
        print("第 %s 页已经下载完成" % time)
        print("--------------------------------")
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
        name_replace = []  # 用户名的格式是用户名+时间，把它两个分开
        name_split = []
        for x in url_name:
            name.append(x.get_text())
        for i in url_text:
            text.append(i.get_text())
        for name_splits in name:
            splits = name_splits.replace("\n","")
            name_replace.append(splits)
        for i in name_replace:
            name_split.append(i.split(" "))
        print("-------------------------------")
        print("正在下载第 %s 页" % time)
        for download in zip(name_split,text):
            try:
                print("Download... %s" % download[0][0])
                with open("baisibudeqijie_text//%s" % (download[0][0]+".txt"),"w") as f:
                    try:
                        f.write(download[1])
                    except UnicodeEncodeError as u:
                        print("你用的可能是windows系统吧~这里报错“GBK”了~用Linux系统吧~")
                        print("或者在cmd窗口下输入: chcp 65001 就可以改成'utf-8'了")
                print("%s Download complite" % download[0][0])
            except urllib.error.HTTPError as f:
                print("图片链接没有找到,可能是被删除了吧～",f.code)
            except FileNotFoundError as e:
                print("段子没有找到，可能是被删除了吧～",e)
        print("第 %s 页已经下载完成" % time)
        print("-------------------------------")
        time+=1



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
                try:
                    urllib.request.urlretrieve(download[1],"baisibudeqijie_audio//%s" % (download[0]+".mp3"))
                    print("%s Download complite!" % download[0])
                except OSError as o:
                    print("文件出错啦~可能是有特殊符号~也有可能是链接消失啦~这张就下载不了啦~",o)
            except UnicodeEncodeError as u:
                print("你用的可能是windows系统吧~这里报错“GBK”了~用Linux系统吧~")
                print("或者在cmd窗口下输入: chcp 65001 就可以改成'utf-8'了",u)
            except urllib.error.HTTPError as f:
                print("图片链接没有找到,可能是被删除了吧～",f.code)
            except FileNotFoundError as e:
                print("没有找到,可能是被删除了吧～",e)
                pass
        print("第 %s 页已经下载完成！" % time)
        print("--------------------------------------")
        time+=1

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
        print("开始下载图片....")
        for download in zip(img_name,img_link):
            try:
                print("Download... %s" % download[0])
                try:
                    urllib.request.urlretrieve(download[1],"baisibudeqijie_peri//baisibudeqijie_peri_img//%s" % (download[0]+"."+download[1][-4:]))
                    print("%s Download complite!" % download[0])
                except OSError as o:
                    print("文件出错啦~可能是有特殊符号~也有可能是链接消失啦~这张就下载不了啦~",o)
            except urllib.error.HTTPError as f:
                print("图片链接没有找到,可能是被删除了吧～",f.code)
            except FileNotFoundError as e:
                print("图片链接没有找到，可能是被删除了吧～",e)
                pass
            for i in img_link:
                if i == img_link[-1]:
                    continue
        print("图片已经下载完成")
        print("------------------------------------")
        print("------------------------------------")
        print("开始下载视频...")
        for downloads in zip(video_name_split[0],video_link):
            try:
                print("Download... %s" % downloads[0])
                try:
                    urllib.request.urlretrieve(downloads[1],"baisibudeqijie_peri//baisibudeqijie_peri_video//%s" % (downloads[0]+"."+downloads[1][-4:]))
                    print("%s Download complite!" % downloads[0])
                except OSError as o:
                    print("文件出错啦~可能是有特殊符号~也有可能是链接消失啦~这张就下载不了啦~",o)
            except urllib.error.HTTPError as f:
                print("图片链接没有找到,可能是被删除了吧～",f.code)
            except FileNotFoundError as e:
                print("视频链接没有找到，可能是被删除了吧～",e)
                pass
        print("视频已经下载完成...")
        print("---------------------------------")
        print("第 %s 页已经下载完成!" % time)

        time+=1


print("--------------------------------")
print("| 1.video                      |")
print("| 2.img                        |")
print("| 3.text                       |")
print("| 4.audio                      |")
print("| 5.peri                       |")
print("--------------------------------")
user = input("请选择1-2-3-4-5: ")

if user == "1":
    print("正在获取页面...")
    try:
        os.mkdir("baisibudeqijie_video")
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
elif user == "4":
    print("正在获取页面...")
    try:
        os.mkdir("baisibudeqijie_audio")
        if os.path.exists("baisibudeqijie_audio"):
            os.rmdir("baisibudeqijie_audio")
            os.mkdir("baisibudeqijie_audio")
    except FileExistsError:
        pass
    audio()
elif user == "5":
    print("正在获取页面...")
    try:
        os.mkdir("baisibudeqijie_peri")
        os.mkdir("baisibudeqijie_peri//baisibudeqijie_peri_img")
        os.mkdir("baisibudeqijie_peri//baisibudeqijie_peri_video") 
        if os.path.exists("baisibudeqijie_peri") and os.path.exists("baisibudeqijie_peri_img") and os.path.exists("baisibudeqijie_peri_video"):
            os.rmdir("baisibudeqijie_peri//baisibudeqijie_peri_img")
            os.rmdir("baisibudeqijie_peri//baisibudeqijie_peri_video")
            os.rmdir("baisibudeqijie_peri")
            os.mkdir("baisibudeqijie_peri")
            os.mkdir("baisibudeqijie_peri_img")
            os.mkdir("baisibudeqijie_peri_video")
    except FileExistsError:
        pass
    peri()
else:
    print("抱歉,选项里没有 '%s'" % user)
