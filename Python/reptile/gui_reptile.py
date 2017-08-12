import urllib.request
from bs4 import BeautifulSoup
import os
import time
from tkinter import *
from tkinter import messagebox
import time, threading
import shutil

class Xxoo():

    def __init__(self):
        self.headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"}

    def get_page(self,url):
        Requesturl = urllib.request.Request(url,headers=self.headers)
        reopen = urllib.request.urlopen(Requesturl)
        Be = BeautifulSoup(reopen.read().decode("utf-8"),'lxml')
        BeSoup = Be.find("span",class_="current-comment-page")
        for Bs in BeSoup:
            return str(Bs)[1:-1]

    def Jandan(self,i):
        select_var = self.var.get()
        url = ["http://jandan.net/ooxx/","http://jandan.net/duan","http://jandan.net/pic"]
        set_flge = ""
        if self.folter_name.get().strip() == "":
            messagebox.showinfo(title="提示",message="请输入文件夹名！")
        else:
            if select_var == 1:
                page = int(self.get_page(url[0]))
                set_flge = "ooxx"
            elif select_var == 2:
                page = int(self.get_page(url[1]))
                set_flge = "duan"
            elif select_var == 3:
                page = int(self.get_page(url[2]))
                set_flge = "pic"
            if not select_var:
                messagebox.showinfo(title="提示",message="抱歉！请选择其中一项！")
            else:
                self.v.set("正在爬取")
            while page >= 0:
                url = "http://jandan.net/{}/page-{}#comments".format(set_flge,page)
                self.txt.insert(END,"正在下载第{}页".format(page))
                Reurl = urllib.request.Request(url,headers=self.headers)
                reopen = urllib.request.urlopen(Reurl)
                Be = BeautifulSoup(reopen.read().decode('utf-8'),'lxml')
                ooxx_and_pic_image_url = Be.find("ol",class_="commentlist").find_all('a',class_="view_img_link")
                issue_name = Be.find('ol',class_="commentlist").find_all("strong")
                content_id = Be.find('ol',class_="commentlist").find_all("span",class_="righttext")
                duan_text = Be.find('ol',class_="commentlist").find_all("p")
                if self.var.get() == 2:
                    self.jandan_dowload(issue_name,content_id,duan_text)
                else:
                    self.jandan_dowload(issue_name,content_id,ooxx_and_pic_image_url)
                if self.stop.get() == "已停止":
                    self.txt.insert(END,"已经停止！")
                    break
                else:
                    self.txt.insert(END,"第{}页下载完成!".format(page))
                    self.txt.insert(END,"\n")
                    if reopen.code != 200:
                        self.state.insert(END,"已完成")
                        self.v.set("爬取")
                        break
                page-=1

    def Doutula(self,i):
        select_var = self.var.get()
        if self.folter_name.get().strip() == "":
            messagebox.showinfo(title="提示",message="请输入文件夹名！")
        else:
            if not select_var:
                messagebox.showinfo(title="提示",message="抱歉！请选择其中一项！")
            else:
                self.v.set("正在爬取")
            if select_var == 4:
                page = 1
                while True:
                    try:
                        os.mkdir("{}".format(self.folter_name.get()))
                    except FileExistsError:
                        if messagebox.askyesno(title="提示",message="文件已经存在,是否删除"):
                            messagebox.showwarning('Yes', '删除成功，并且重新创建完成！')
                            shutil.rmtree(self.folter_name.get())
                            os.mkdir(self.folter_name.get())
                        else:
                            messagebox.showinfo('No', '已经停止下载，请重新输入文件夹名!')
                            self.v.set("爬取")
                            break
                    self.txt.insert(END,"正在下载第{}页".format(page))
                    article_url = "https://www.doutula.com/article/list/?page={}".format(page)
                    Requesturl = urllib.request.Request(article_url,headers=self.headers)
                    reopen = urllib.request.urlopen(Requesturl)
                    BeSoup = BeautifulSoup(reopen.read().decode("utf-8"),'lxml')
                    get_article_page_link = BeSoup.find("div",class_="col-sm-9").find_all("a")   # 套图的链接
                    article_issue_tag = BeSoup.find('div',class_="col-sm-9").find_all("div",class_="random_title")  # 套图的名称,用做保存文件夹的名字
                    for info_img in zip(get_article_page_link[0:10],article_issue_tag):
                        # print(info_img[1].get_text())
                        self.txt.insert(END,"正在下载 {} 的套图".format(info_img[1].get_text()))
                        os.mkdir("{}/{}".format(self.folter_name.get(),info_img[1].get_text()))
                        img_Request = urllib.request.Request(info_img[0]['href'],headers=self.headers)
                        img_urlopen = urllib.request.urlopen(img_Request)
                        BS = BeautifulSoup(img_urlopen.read().decode("utf-8"),'lxml')
                        get_img_and_name = BS.find('div',class_="col-sm-9").find_all('img')
                        for dowload in get_img_and_name:
                            try:
                                if dowload['src'][0:5] == 'http:':
                                    self.txt.insert(END,"√ 名字: {} 地址: {} OK".format(dowload['alt'],dowload['src']))
                                    urllib.request.urlretrieve(dowload['src'],"{}/{}/{}".format(self.folter_name.get(),info_img[1].get_text(),dowload['alt']+dowload['src'][-4:]))
                                else:
                                    self.txt.insert(END,"√ 名字: {} 地址: {} OK".format(dowload['alt'],dowload['src']))
                                    urllib.request.urlretrieve("http:"+dowload['src'],"{}/{}/{}".format(self.folter_name.get(),info_img[1].get_text(),dowload['alt']+dowload['src'][-4:]))
                            except FileNotFoundError:
                                os.mkdir(self.folter_name.get())
                        if self.stop.get() == "已停止":
                            break
                    if self.stop.get() == "已停止":
                        self.txt.insert(END,"已经停止！")
                        break
                    else:
                        self.txt.insert(END,"第{}页下载完成!".format(page))
                        self.txt.insert(END,"\n")
                        if reopen.code != 200:
                            self.state.insert(END,"已完成")
                            self.v.set("爬取")
                            break
                        page+=1
            elif select_var == 5:
                page = 1
                while True:
                    self.txt.insert(END,"正在下载第{}页".format(page))
                    photo_url = "https://www.doutula.com/photo/list/?page={}".format(page)
                    Requesturl = urllib.request.Request(photo_url,headers=self.headers)
                    reopen = urllib.request.urlopen(Requesturl)
                    BeSoup = BeautifulSoup(reopen.read().decode("utf-8"),'lxml')
                    get_photo_page_link = BeSoup.find("div",class_="page-content text-center").find_all("a")   # 表情的链接
                    # photo_issue_tag = BeSoup.find("div",class_="page-content text-center").find_all("p")  # 表情的名称，用做保存文件的名字
                    try:
                        os.mkdir("{}".format(self.folter_name.get()))
                    except FileExistsError:
                        if messagebox.askyesno(title="提示",message="文件已经存在,是否删除"):
                            messagebox.showwarning('Yes', '删除成功，并且重新创建完成！')
                            shutil.rmtree(self.folter_name.get())
                            os.mkdir(self.folter_name.get())
                        else:
                            messagebox.showinfo('No', '已经停止下载，请重新输入文件夹名!')
                            self.v.set("爬取")
                            break
                        # print(panduan)
                    for info_img in get_photo_page_link:
                        img_Request = urllib.request.Request(info_img['href'],headers=self.headers)
                        img_urlopen = urllib.request.urlopen(img_Request)
                        Bs = BeautifulSoup(img_urlopen.read().decode("utf-8"),'lxml')
                        get_img_and_name = Bs.find('div',class_="col-xs-12 col-sm-6 artile_des").find_all('img')
                        for dowload in get_img_and_name:
                                self.txt.insert(END,"√ 简称: {} 地址: {} OK".format(dowload['alt'],"https:"+dowload['src']))
                                try:
                                    urllib.request.urlretrieve("https:"+dowload['src'],"{}/{}".format(self.folter_name.get(),dowload['alt'][0:30]+dowload['src'][-4:]))
                                except:
                                    pass
                        if self.stop.get() == "已停止":
                            break
                    if self.stop.get() == "已停止":
                        self.txt.insert(END,"已经停止！")
                        break
                    else:
                        self.txt.insert(END,"第{}页下载完成!".format(page))
                        self.txt.insert(END,"\n")
                        if reopen.code != 200:
                            self.state.insert(END,"已完成")
                            self.v.set("爬取")
                            break
                        page+=1
            else:
                pass

    def Budejie(self,i):
        select_var = self.var.get()
        if self.folter_name.get().strip() == "":
            messagebox.showinfo(title="提示",message="请输入文件夹名！")
        else:
            self.v.set("正在爬取")
            if select_var == 6:
                page = 1
                try:
                    os.mkdir("{}".format(self.folter_name.get()))
                except FileExistsError:
                    pass
                while True:
                    self.txt.insert(END,"正在下载第{}页".format(page))
                    photo_url = "http://www.budejie.com/video/{}".format(page)
                    Requesturl = urllib.request.Request(photo_url,headers=self.headers)
                    openurl = urllib.request.urlopen(Requesturl)
                    Besoup = BeautifulSoup(openurl.read().decode("utf-8"),'lxml')
                    Be_link = Besoup.find("div",class_="j-r-c").find_all("a",class_="ipad-down-href")
                    Be_tag = Besoup.find("div",class_="j-r-c").find_all("li",class_="j-r-list-tool-l-down f-tar j-down-video j-down-hide ipad-hide")
                    Be_name = Besoup.find("div",class_="j-r-c").find_all("a",class_="u-user-name")
                    for dowload in zip(Be_link,Be_tag,Be_name):
                        try:
                            self.txt.insert(END,"标题: {} 地址: {}".format(dowload[1]['data-text'],dowload[0]['href']))
                            urllib.request.urlretrieve(dowload[0]['href'],"{}/{}".format(self.folter_name.get(),dowload[1]['data-text'][0:30]+dowload[0]['href'][-4:]))
                        except OSError:
                            self.txt.insert(END,"标题: {} 地址: {}".format(dowload[1]['data-text'],dowload[0]['href']))
                            urllib.request.urlretrieve(dowload[0]['href'],"{}/{}".format(self.folter_name.get(),dowload[2].get_text()+dowload[0]['href'][-4:]))
                        if self.stop.get() == "已停止":
                            break
                    if self.stop.get() == "已停止":
                        self.txt.insert(END,"已经停止！")
                        break
                    else:
                        self.txt.insert(END,"第{}页下载完成!".format(page))
                        self.txt.insert(END,"\n")
                        if openurl.code != 200:
                            self.state.insert(END,"已完成")
                            self.v.set("爬取")
                            break
                    page+=1
            else:
                messagebox.showinfo(title="提示",message="抱歉~网络故障！？")
                self.v.set("爬取")

    def jandan_dowload(self,name,content_id,img_or_text):
        if self.var.get() == 2:
            for dowload in zip(name,content_id,img_or_text):
                try:
                    self.txt.insert(END,"√ 作者:{} 图片ID:{} 内容:{}  OK!".format(dowload[0].get_text(),dowload[1].get_text(),dowload[2].get_text()[0:20]+"......"))   # 作者名字有些是乱码~tkinter不接受~
                    with open("{}/{}".format(self.folter_name.get(),dowload[0].get_text()+dowload[1].get_text()+".txt"),'w') as save:
                        save.write(dowload[2].get_text())
                    time.sleep(0.001) 
                except:
                    self.txt.insert(END,"√ 图片ID:{} 内容:{}  OK!".format(dowload[1].get_text(),dowload[2].get_text()[0:20]+"......"))   #如果作者名字有特殊字符的~就在tkinter中去掉作者的名字,但是下载之后是正常显示的~
                    time.sleep(0.001)
                try:
                    with open("{}/{}".format(self.folter_name.get(),dowload[0].get_text()+dowload[1].get_text()+".txt"),'w') as save:
                        try:
                            save.write(dowload[2].get_text())
                        except UnicodeEncodeError:
                            pass
                except FileNotFoundError:
                    os.mkdir(self.folter_name.get())
        else:
            for dowload in zip(name,content_id,img_or_text):
                try:
                    self.txt.insert(END,"√ 作者:{} 图片ID:{} 图片地址:{}  OK!".format(dowload[0].get_text(),dowload[1].get_text(),"http:"+dowload[2]['href']))   # 作者名字有些是乱码~tkinter不接受~
                    urllib.request.urlretrieve('http:'+dowload[2]['href'],'{}/{}'.format(self.folter_name.get(),dowload[0].get_text()+dowload[1].get_text()+dowload[2]['href'][-4:]))
                    time.sleep(0.001) 
                except:
                    self.txt.insert(END,"√ 图片ID:{} 图片地址:{}  OK!".format(dowload[1].get_text(),"http:"+dowload[2]['href']))   #如果作者名字有特殊字符的~就在tkinter中去掉作者的名字,但是下载之后是正常显示的~
                    time.sleep(0.001)
                try:
                    urllib.request.urlretrieve('http:'+dowload[2]['href'],'{}/{}'.format(self.folter_name.get(),dowload[0].get_text()+dowload[1].get_text()+dowload[2]['href'][-4:]))
                except FileNotFoundError:
                    os.mkdir(self.folter_name.get())


    def thread_dowload(self):
        self.stop.set("停止")
        select_var = self.var.get()
        if select_var in [1,2,3]:
            for i in range(1):
                th=threading.Thread(target=self.Jandan,args=(i,))  
                th.setDaemon(True)
                th.start()
        elif select_var in [4,5]:
            for i in range(1):
                th=threading.Thread(target=self.Doutula,args=(i,))
                th.setDaemon(True)
                th.start()
        elif select_var in [6,7,8,9,10]:
            for i in range(1):
                th=threading.Thread(target=self.Budejie,args=(i,))
                th.setDaemon(True)
                th.start()
        else:
            messagebox.showinfo(title="提示",message="抱歉！请选择其中一项！")

    def Stop(self): 
        if self.v.get() == "爬取":
            messagebox.showinfo(title="提示",message="你还没开始呢,就要结束了?")
        else:
            self.stop.set("已停止")
            clear = StringVar()
            remdir_folter = StringVar()
            clear.set("清除")
            clear_bt = Button(self.root,font=("楷体",15),textvariable=clear,command=self.clear,relief="solid",bg="#444").place(x=790,y=450)
            self.v.set("爬取")
            remdir_folter.set("删除目录")
            rmdir_folter = Button(self.root,font=("楷体",10),textvariable=remdir_folter,command=self.Rmdir_folter,relief="solid",bg="#444").place(x=520,y=595)

    def clear(self):
        self.txt.delete(0,END)
        self.state.delete(0,END)

    def Rmdir_folter(self):
        try:
            shutil.rmtree(self.folter_name.get())
            messagebox.showinfo(title="提示",message="删除成功!")
        except FileNotFoundError:
            messagebox.showinfo(title="提示",message="文件夹不存在!")

    def folter(self):
        if self.folter_name.get().strip() == "":
            pass
        else:
            self.abspath.set(os.path.abspath(".")+'\\'+self.folter_name.get())


    def main(self):
        self.root = Tk()
        self.root.geometry("900x650")
        self.root.maxsize("900","650")
        self.root.minsize("900","650")
        self.root.title("Crazy Rookie www.liuyangxiong.top")
        self.root.config(bg="#333")
        jiandan_img = PhotoImage(file="jiandan.jpg")
        budejie_img = PhotoImage(file="logo_new.png")
        doutula_img = PhotoImage(file="doutula.png")
        Label(self.root,image=jiandan_img,bg="#333",fg="#996",font=("宋体",50)).place(x=20,y=20)
        Label(self.root,image=doutula_img,bg="#993",fg="#996",font=("宋体",50)).place(x=270,y=20)
        Label(self.root,image=budejie_img,bg="#333",fg="#996",font=("宋体",50)).place(x=650,y=20)
        self.var = IntVar()
        self.v = StringVar()
        self.stop = StringVar()
        self.abspath = StringVar()
        self.folter_name = StringVar()
        self.v.set("爬取")
        self.stop.set("停止")
        jiandan_meizhi = Radiobutton(self.root,text="妹子图",variable=self.var,value=1,bg="#444",relief="solid",font=("宋体",15),indicatoron=0).place(x=20,y=120)
        jiandan_duan = Radiobutton(self.root,text="段子",variable=self.var,value=2,bg="#444",relief="solid",font=("宋体",15),indicatoron=0).place(x=100,y=120)
        jiandan_pic = Radiobutton(self.root,text="无聊图",variable=self.var,value=3,bg="#444",relief="solid",font=("宋体",15),indicatoron=0).place(x=20,y=160)
        doutula_article_list = Radiobutton(self.root,text="最新套图",variable=self.var,value=4,bg="#444",relief="solid",font=("宋体",15),indicatoron=0).place(x=270,y=140)
        doutula_photo_list = Radiobutton(self.root,text="最新表情",variable=self.var,value=5,bg="#444",relief="solid",font=("宋体",15),indicatoron=0).place(x=370,y=140)
        budejie_video = Radiobutton(self.root,text="视频",variable=self.var,value=6,bg="#444",relief="solid",font=("宋体",15),indicatoron=0).place(x=670,y=120)
        budejie_pic = Radiobutton(self.root,text="图片",variable=self.var,value=7,bg="#444",relief="solid",font=("宋体",15),indicatoron=0).place(x=730,y=120)
        budejie_text= Radiobutton(self.root,text="段子",variable=self.var,value=8,bg="#444",relief="solid",font=("宋体",15),indicatoron=0).place(x=790,y=120)
        budejie_audio = Radiobutton(self.root,text="声音",variable=self.var,value=9,bg="#444",relief="solid",font=("宋体",15),indicatoron=0).place(x=670,y=160)
        budejie_tag = Radiobutton(self.root,text="美女",variable=self.var,value=10,bg="#444",relief="solid",font=("宋体",15),indicatoron=0).place(x=730,y=160)
        scrollbar = Scrollbar(self.root)
        scrollbar.pack( side = RIGHT, fill=Y )
        self.txt=Listbox(self.root,width=126,height=24,selectmode="extended",yscrollcommand=scrollbar.set)
        Button(self.root,command=self.thread_dowload,font=("楷体",15),textvariable=self.v,relief="solid",bg="#444").place(x=790,y=250)
        stop_bt = Button(self.root,command=self.Stop,font=("楷体",15),textvariable=self.stop,relief="solid",bg="#444").place(x=790,y=300)
        self.txt=Listbox(self.root,width=126,height=24,selectmode="extended",relief="solid",bg="#222",fg="#999")
        self.txt.place(x=20,y=200)
        self.txt.delete(1,10)
        states = Label(self.root,text="状态:",font=("楷体",15),bg="#333").place(x=730,y=600)
        self.state = Listbox(self.root,width=10,height=1)
        self.state.place(x=790,y=605)
        Label(self.root,text="文件夹所在位置:",font=("楷体",15),bg="#333").place(x=20,y=620)
        Label(self.root,text="文件夹名字:",font=("楷体",15),bg="#333").place(x=60,y=595)
        Button(self.root,command=self.folter,font=("楷体",10),text="确认",relief="solid",bg="#444").place(x=400,y=595)
        self.folter_name = Entry(self.root,font=("楷体",15),bg="#666",relief="solid",fg="#000")
        self.folter_name.place(x=175,y=595)
        Entry(self.root,width=65,font=("楷体",12),bg="#000",relief="solid",fg="#893333",textvariable=self.abspath).place(x=175,y=623)
        self.root.mainloop()
        

if __name__ == '__main__':
    if os.path.exists("doutula.png") == True and os.path.exists("jiandan.jpg") == True and os.path.exists("logo_new.png") == True:
        X = Xxoo()
        X.main()
    else:
        img_url = ["http://obf6hf3q0.bkt.clouddn.com/jiandan.jpg","http://obf6hf3q0.bkt.clouddn.com/logo_new.png","http://obf6hf3q0.bkt.clouddn.com/doutula.png"]
        for dowload_img in img_url:
            urllib.request.urlretrieve(dowload_img,dowload_img.split("/")[-1])
        X = Xxoo()
        X.main()