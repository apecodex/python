from tkinter import *
import os

class QQ_daogao():

    def __init__(self):
        self.windows = Tk()

    def callback(self,event=None):
        pass
    def main(self):
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
        self.windows.config(bg="#00BFFF")
        self.windows.overrideredirect(True)
        image = PhotoImage(file="head.png",width=100,height=100)
        cv =  Canvas(self.windows,bg="#e8f0fb")
        cv.configure(width=500)
        cv.configure(height=150)
        cv.create_image(70,50,image=image)
        # cv.create_line(0,100,50,50,width=10)
        # cv.create_oval(15,15,100,100,fill="#FFF")
        cv.place(x=0,y=180)
        exit_btn = Button(self.windows,text="X",font=("楷体",10),command=self.windows.quit,bg="#00BFFF",activebackground="red",relief="flat").place(x=395,y=-5)
        # Label(self.windows,bg="#F5FAFF",width="80",height="8").pack(side="bottom")
        user = Entry(self.windows,font=("微软雅黑",12),relief="flat")
        user.place(x=130,y=195)
        password = Entry(self.windows,font=("微软雅黑",12),relief="flat")
        password.place(x=130,y=225)
        login_btn = Button(self.windows,text="登   录".center(46),fg="#FFF",activebackground="#87CEFA",bg="#00BFFF",font=("微软雅黑",10),relief="flat").place(x=130,y=280)
        self.windows.mainloop()


if __name__ == '__main__':
    q = QQ_daogao()
    q.main()