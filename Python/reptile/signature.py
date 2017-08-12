import urllib.request
import re
from tkinter import *
from tkinter import messagebox
from PIL import Image
import time, threading

def downloading(name,var):
    url = "http://www.uustv.com/"
    html_Request = urllib.request.Request(url,data="word={}&sizes=60&fonts={}&fontcolor=%23000000".format(name,var).encode("utf-8"))
    html_open = urllib.request.urlopen(html_Request).read().decode("utf-8")
    res = '<div class="tu">﻿<img src="(.*?)"/></div>'
    re_html = re.findall(res,html_open)
    urllib.request.urlretrieve(url+re_html[0],"%s.gif" % name)
    try:
        open_img = Image.open("%s.gif" % name)
        open_img.show()
        open_img.close()
    except :
        messagebox.showinfo(title="提示",message="请自行打开!")


def get_name():
    name = names.get()
    select_var = var.get()
    signature_ttf = ["jfcs.ttf","qmt.ttf","bzcs.ttf","lfc.ttf","haku.ttf","zql.ttf","yqk.ttf"]
    if not name:
        messagebox.showinfo(title="提示",message="姓名不得为空!")
    elif select_var == 1:
        downloading(name,signature_ttf[0])
    elif select_var == 2:
        downloading(name,signature_ttf[1])
    elif select_var == 3:
        downloading(name,signature_ttf[2])
    elif select_var == 4:
        downloading(name,signature_ttf[3])
    elif select_var == 5:
        downloading(name,signature_ttf[4])
    elif select_var == 6:
        downloading(name,signature_ttf[5])
    elif select_var == 7:
        downloading(name,signature_ttf[6])
    else:
        messagebox.showinfo(title="提示",message="请选择您想要的样式!")

def fun():  
    th=threading.Thread(target=get_name) 
    th.setDaemon(True)
    th.start()

if __name__ == '__main__':
    MainWindows = Tk()
    MainWindows.geometry("400x250")
    MainWindows.maxsize("400","250")
    MainWindows.minsize("400","250")
    MainWindows.title("个性签名")
    MainWindows.config(bg="#444")
    Label(MainWindows,text="姓名: ",font=("楷体",20),bg="#444",fg="#fff").place(x=50,y=50)
    names = Entry(MainWindows,font=("楷体",20),fg="#666",width=15)
    names.place(x=140,y=50)
    var = IntVar()
    rb1 = Radiobutton(MainWindows,text="个性签",variable=var,value=1,bg="#444",relief="solid").place(x=50,y=115)
    rb2 = Radiobutton(MainWindows,text="连笔签",variable=var,value=2,bg="#444",relief="solid").place(x=50,y=150)
    rb3 = Radiobutton(MainWindows,text="潇洒签",variable=var,value=3,bg="#444",relief="solid").place(x=50,y=185)
    rb4 = Radiobutton(MainWindows,text="草体签",variable=var,value=4,bg="#444",relief="solid").place(x=50,y=220)
    rb5 = Radiobutton(MainWindows,text="合文签",variable=var,value=5,bg="#444",relief="solid").place(x=150,y=115)
    rb6 = Radiobutton(MainWindows,text="商务签",variable=var,value=6,bg="#444",relief="solid").place(x=150,y=150)
    rb7 = Radiobutton(MainWindows,text="可爱签",variable=var,value=7,bg="#444",relief="solid").place(x=150,y=185)
    Button(MainWindows,text="一键设计",font=("楷体",15),relief="solid",command=fun).place(x=280,y=200)
    MainWindows.mainloop()
