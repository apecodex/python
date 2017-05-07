# -*- coding: utf-8 -*-

import json
import hashlib
import os
import getpass
from random import randint
import re
import time
import sqlite3


# 连接数据库
def sql_db():
    connect_sql = sqlite3.connect("guess_number.db")
    cursor = connect_sql.cursor()
    date = """
    CREATE TABLE user(
    id INTEGER UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(65) UNIQUE NOT NULL,
    password CHAR(65) NOT NULL,
    mail VARCHAR(32) UNIQUE NOT NULL,
    `time` DATETIME
    );

    CREATE TABLE administrator(
    id INTEGER UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id INTEGER UNSIGNED,
    create_time DATETIME,
    FOREIGN KEY (user_id) REFERENCES user (id)
    );

    CREATE TABLE players_message(
    id INTEGER UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id INTEGER UNIQUE,
    game_time DATETIME,
    second VARCHAR(32) DEFAULE 0,
    total_input VARCHAR(255) DEFAULE '[]',
    mode VARCHAR(32) DEFAULE 'NO',
    FOREIGN KEY (user_id) REFERENCES user (id)
    );
    """
    try:
        cursor.executescript(date)
    except sqlite3.OperationalError as f:
        print(f)
    cursor.close()
    connect_sql.commit()
    connect_sql.close()


# 操作sql
class Options_sql():

    #连接初始化
    def __init__(self):
        self.connect_sql = sqlite3.connect("guess_number.db")
        self.cursor = self.connect_sql.cursor()

    #获取本地时间
    def get_time(self):
        return str(time.localtime()[0])+'-'+str(time.localtime()[1])+'-'+str(time.localtime()[2])+'-'+str(time.localtime()[3])+'-'+str(time.localtime()[4])+'-'+str(time.localtime()[5])
    #添加玩家数据
    def add_sql(self,name,password,mail):
        ids = []
        message_id = []
        get_max_id = self.cursor.execute("SELECT * FROM user WHERE id=(SELECT MAX(id) from user);")
        get_message_max_id = self.cursor.execute("SELECT * FROM players_message WHERE id=(SELECT MAX(id) from user);")
        for i in get_max_id:
            ids.append(i[0])
        for m in get_message_max_id:
            message_id.append(m[0])
        data = """
        INSERT INTO user (id,name,password,mail,`time`) VALUES ({},'{}','{}','{}','{}');
        """.format(ids[0]+1,name,password,mail,self.get_time())
        date_message = """
        INSERT INTO players_message (id,user_id,game_time,second,total_input,mode) VALUES ({},{},'{}',{},'{}','{}')
        """.format(message_id[0]+1,ids[0]+1,'0000-00-00-00-00',,,)
        self.cursor.execute(data)
        self.cursor.close()
        self.connect_sql.commit()
        self.connect_sql.close()

    #添加管理员数据
    def add_admin(self,name,password,mail,create_time):
        user_id = []
        admin_id = []
        get_user_max_id = self.cursor.execute("SELECT * FROM user WHERE id=(SELECT MAX(id) from user);")
        get_admin_max_id = self.cursor.execute("SELECT * FROM administrator WHERE id=(SELECT MAX(id) from administrator);")
        for i in get_user_max_id:
            user_id.append(i[0])
        for i in get_admin_max_id:
            admin_id.append(i[0])
        data = """
        INSERT INTO user (id,name,password,mail,'time') VALUES ({},'{}','{}','{}','{}');
        """.format(user_id[0]+1,name,password,mail,self.get_time)
        admin_data = """
        INSERT INTO administrator (id,user_id,create_time) VALUES ({},{},'{}');
        """.format(admin_id[0]+1,user_id[0]+1,self.get_time)
        self.cursor.execute(data)
        self.cursor.execute(admin_data)
        self.cursor.close()
        self.connect_sql.commit()
        self.connect_sql.close()

    # 存储用户的游戏数据
    def players_data(self,name,game_time,second,total_input,mode):
        message_id = []
        find_uid = """
        SELECT id FROM players_message WHERE user_id=(SELECT id FROM user WHERE name='{}');
        """.format(name)
        players_message_id = self.cursor.execute(find_uid)
        get_max_id = self.cursor.execute("SELECT MAX(id) FROM players_message;")
        for m in get_max_id:
            message_id.append(m[0])
        save_data = """
        INSERT INTO players_message (id,user_id,game_time,second,total_input,mode) VALUES ({},{},'{}',{},'{}','{}')
        """.format(message_id[0],players_message_id,game_time,second,total_input,mode)
        self.cursor.execute(save_data)
        self.cursor.close()
        self.connect_sql.commit()
        self.connect_sql.close()


    #删除用户（ROOT）
    def root_pop_sql(self,name):
        delete_user = "DELETE FROM user WHERE id=(SELECT id FROM user WHERE name='{}')".format(name)
        delete_admin = "DELETE FROM administrator WHERE user_id=(SELECT id FROM name='{}'')".format(name)
        delete_players_message = "DELETE FROM players_message WHERE user_id=(SELECT id FROM user WHERE name='{}')".format(name)
        self.cursor.execute(delete_user)
        self.cursor.execute(delete_admin)
        self.cursor.execute(delete_players_message)
        self.cursor.close()
        self.connect_sql.commit()
        self.connect_sql.clsoe()

    #删除用户 (administrator)
    def admin_pop_sql(self,name):
        get_id = self.cursor.execute("SELECT")

    def get_user_game_message(self,name):
        pass


# 加密密码
def hasd_md5(user,password):
    md5 = hashlib.md5()
    md5.update((user+password+"Guess*Number").encode())
    return md5.hexdigest()

# 查看游戏的历史记录
def cat_game_history(name):
    with open("game_date/"+name+".txt",'r') as cat_file:
        if os.name == "posix":
            os.system("gedit game_date/{}.txt".format(name))
        else:
            print(cat_file.read())
# 登录系统
class Register:
    # 注册
    def register(self):
        print("------------------------------")
        print("|  ~Registration interface~  |")
        print("------------------------------")
        with open("user_date.txt",'r') as u:   # 获取本地文本文件里的用户数据(用户名和密码)
            user_name = json.load(u)
        with open("user_mail.txt") as m:     # 同上，获取本地用户的用户名和邮箱(两个都是dict)
            user_main = json.load(m)
            while True:
                print("Enter q to exit the registration")
                get_mail = [i for i in user_main.values()]  # 得到邮箱
                new_name = input("New name: ")
                if new_name == "q" or new_name == "Q":
                    print("Unregistered!")
                    Re = Register()
                    Re.Login()
                    break
                new_password = getpass.getpass("New Password: ")
                again_password = getpass.getpass("Again Password:")
                new_mail = input("Mail: ")
                password_chack = [i for i in new_password if i.isalpha()]   # 检查密码里面有没有带字母，没有就是[]空list
                mail_split = new_mail.split("@")      # 将邮箱拆成两半
                mail_re = re.findall(r'[^a-z0-9]+',mail_split[0])     # 匹配,有数字和字母都ok,其他都不要
                if len(new_name.split()) != 1 or (new_name.strip() == new_name) == False:  # 用户名中不能有空格
                    print("user name not have strip")
                elif new_password != again_password:    # 判断两次的密码是否相同
                    print("Twice the password is not the same, please re-enter!")
                    continue
                elif new_name in user_name:    # 检查 新的用户名有没有在本地数据库中
                    print("username already exists!")
                    continue
                elif len(new_password) <= 6 or password_chack == []:    # 密码长度不能小于6位数，并且至少有一个字母
                    print("Password is too weak. Please enter at least 6 digits and at least 1 letter")
                elif new_mail in get_mail:     # 检查 邮箱有没有被注册
                    print("'%s' The mailbox is already registered!" % new_mail)
                elif mail_re != [] or mail_split[-1] not in ["qq.com","gmail.com","163.com"]:   #检查 用户输入的邮箱格式对不对
                    print("please enter your vaild email")
                else:
                    get_user_md5 = hasd_md5(new_name, new_password)
                    user_name[new_name] = get_user_md5  # 数据库里面的都是dict
                    user_main[new_name] = new_mail
                    with open("user_date.txt",'w') as f:
                        json.dump(user_name,f)   # 重新写入本地数据库
                    if os.name == "posix":
                        os.system(r"echo > game_date/{}.txt".format(new_name))   # 在注册成功的同时将用户的Game数据创建了～
                    else:
                        open("game_date/{}.txt".format(new_name),'w')   # 如果是windows系统
                    print("%s Created successfully！" % new_name)  # 创建成功！
                    with open("date.txt",'a') as d:    # 将创建成功的时间写入'date.txt'
                        d.write("\n--------------------------------------------------------------------------\n")
                        d.write("time:{} user'{}'Joined here".format(time.ctime(),new_name))
                        d.write("\n--------------------------------------------------------------------------\n\n")
                    with open("game_date/"+new_name+".txt",'w') as f:   # 把数据写入用户自己命名的文本文件中
                        f.write("----------------------------------------------------------------------------\n")
                        f.write("Dear'{}',You are welcome to join us!\n".format(new_name))
                        f.write("Registration time: ")
                        f.write(time.ctime())
                        f.write("\n---------------------------------------------------------------------------\n\n\n")
                    with open("user_mail.txt",'w') as s:     # 把邮箱写入'user_mail.txt'
                        json.dump(user_main,s)
                        return "A"     # 这里返回A是为了注册完后可以直接登录
                        break
    # 找回密码
    def Find_password(self):
        print("------------------------")
        print("| ～Find the password～ |")
        print("------------------------")
        with open("user_mail.txt",'r') as f:
            user_mail = json.load(f)
        with open("user_date.txt",'r') as d:
            user_name = json.load(d)
        with open("root_mail.txt",'r') as rm:
            root_mail = json.load(rm)
        with open("administrator.txt",'r') as r:
            roots = json.load(r)
            while True:
                name = input("user name: ")
                mail = input("Mail: ")
                if name in roots and mail == root_mail[name]:
                    while True:
                        New_password = getpass.getpass("New Password: ")
                        again_password = getpass.getpass("Again Password: ")
                        get_new_md5 = hasd_md5(name, New_password)     # 得到新的md5值
                        if New_password == again_password:
                            user_name[name] = get_new_md5
                            print("Successfully modified！")
                            with open("user_date.txt",'w') as n:     # 将新的数据写入数据库
                                json.dump(user_name,n)
                            with open("administrator.txt",'w') as rs:
                                json.dump(user_name,rs)
                                break
                        else:
                            print("The password is not the same twice!")
                    break
                elif name in user_name and mail == user_mail[name]:     # 判断用户名和邮箱和数据库的合不合
                    while True:
                        New_password = getpass.getpass("New Password: ")
                        again_password = getpass.getpass("Again Password: ")
                        get_new_md5 = hasd_md5(name, New_password)     # 得到新的md5值
                        if New_password == again_password:
                            user_name[name] = get_new_md5
                            print("Successfully modified！")
                            with open("user_date.txt",'w') as n:     # 将新的数据写入数据库
                                json.dump(user_name,n)
                                break
                        else:
                            print("The password is not the same twice!")
                    break
                else:
                    print("User name or mailbox error")
    # 主函数，登录
    def Login(self):
        print("Login System!")
        print("----------------------")
        print("|  ~Login Interface~ |")
        print("----------------------")
        while True:
            print("Any key to continue to log in, enter 'q' to cancel the login")
            s = input(">>> ")
            if s == "q" or s == "Q":
                print("Sign-in canceled")
                break
            with open("user_date.txt",'r') as u:  # 获取用户的数据
                user_date = json.load(u)
                name = input("User name: ")
                password = getpass.getpass("password: ")
                get_password_md5 = hasd_md5(name,password)
                if name not in user_date:
                    print("User name% s does not exist! \n Any key to continue registration, 'q' to exit" % name)
                    seleste = input(">>> ")      # 退出注册！
                    if seleste == "q":
                        print("Quits!")
                        Re = Register()
                        Re.Login()
                        break
                    print("REGISTERED!")     # 除了输入'q'以外的继续注册
                    Re = Register()
                    Re.register()
                else:
                    if name in user_date and user_date[name] == get_password_md5:     # 判断用户输入的密码是否与数据库的相同
                        print("Welcome %s" % name)
                        with open("date.txt",'a') as d:   # 如果登录成功,则把登录时间写入'date.txt'
                            d.write("\n\n************************************************************\n")
                            d.write("time:{},user'{}'Login game".format(time.ctime(),name))
                            d.write("\n************************************************************\n")
                        print("Dear'%s',Welcome！" % name)
                        while True:
                            print("------------------")
                            print("-------Menu Bar--------")
                            print("| 1.Start a new game  |")
                            print("| 2.View history      |")
                            print("| 3.sign out          |")
                            print("-----------------------")
                            user_input = input("1-2-3")
                            if user_input == "1":
                                game = Game_date()
                                game.main(name)
                                stop()
                                continue
                            elif user_input == "2":
                                cat_game_history(name)
                                stop()
                                continue
                            elif user_input == "3":
                                print("{}，Signed out!".format(name))
                                with open("date.txt",'a') as f:
                                    f.write("\n\nXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n")
                                    f.write("time:{},user'{}'Logged out!".format(time.ctime(),name))
                                    f.write("\nXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n")
                                break
                            else:
                                print("Sorry, there is no option '%s'" % user_input)
                                continue
                            break
                    else:
                        print("Account or password error, whether to retrieve the password？(y/n)")
                        enter = str(input(">>> "))
                        if enter == "Y" or enter == "y":    #如果密码错误，可选择找回密码（重新设置）
                            print("Find the password")
                            Ref = Register()
                            Ref.Find_password()
                        else:
                            continue
# 游戏
class Game_date:

    def main(self,name):
        print("Start Game!")
        print("------------------------")
        print("|   ~game interface~   |")
        print("------------------------")
        cishu = 1
        generate_list = []    # 存储用户输入的每一个数字
        compute_total = {}    # 存储用户输入的重复数字，比如 2 输入了两次就是{"2"：2}
        suijishu1 = randint(0,20)   # 获取随机数
        suijishu2 = randint(0,50)
        suijishu3 = randint(0,100)
        last_dict = {}    # 存储最后重复过的总数,比如 2 最后所输入的6次,就是{"2":6}
        get_list = []     # 得到输入的次数
        print("Select Difficulty: ")
        print("````````````````")
        print("| 1.simple     |")
        print("| 2.general    |")
        print("| 3.difficult  |")
        print("````````````````")
        while True:
            user = input(">>> ")
            if user == "1":
                print("~~~~~Simple mode~~~~~")
                print("Please enter an integer no greater than 20 and no less than 0")
                with open("date.txt",'a') as d1:
                    d1.write("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
                    d1.write("time:{}\n".format(time.ctime()))
                    d1.write("user'{}',Play'{}'the game".format(name,"Simple mode"))
                    d1.write("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
                break
            elif user == "2":
                print("~~~~~General Mode~~~~~")
                print("Please enter an integer no greater than 50 and no less than 0")
                with open("date.txt", 'a') as d2:
                    d2.write("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
                    d2.write("time:{}\n".format(time.ctime()))
                    d2.write("user'{}',Play'{}'the game".format(name, "General Mode"))
                    d2.write("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
                    break
            elif user == "3":
                print("~~~~~Difficult mode~~~~~")
                print("Please enter an integer no greater than 100 and no less than 0")
                with open("date.txt",'a') as d3:
                    d3.write("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
                    d3.write("time:{}\n".format(time.ctime()))
                    d3.write("user'{}',Play'{}'the game".format(name,"Difficult mode"))
                    d3.write("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
                break
            else:
                print("sorry, we do not have that{}".format(user))
                continue
        print("Are you ready?")
        input("Any key to start the game...")
        print("Game Start!!!")
        start = time.time()
        while True:
            user_input = input(">>> ")
            generate_list.append(user_input)
            s = generate_list.count(user_input)
            compute_total[user_input]=s
            not_reast = set([i for i in generate_list if generate_list.count(i) > 1])  # 没有重复的数字
            get_num1 = [i for i in generate_list if i.strip() and i.isnumeric() and int(i) < 21]   # 只能有数字，其他的都不要～(难度1)
            get_num2 = [i for i in generate_list if i.strip() and i.isnumeric() and int(i) < 51]   # 同上，50以内(难度一般)
            get_num3 = [i for i in generate_list if i.strip() and i.isnumeric() and int(i) < 101]  # 100以内(难度困难)
            try:
                for i in not_reast:
                    f = compute_total[i]
                    get_list.append(f)
                    last_dict[i]=get_list[-1]
                if user_input.isnumeric() == False:
                    last_dict.pop(user_input)
            except KeyError:
                pass
            try:
                new_user = int(user_input)  #
            except ValueError:
                compute_total.pop(user_input)
                print("Please enter an integer")
                cishu-1
                continue
            if user == "1":
                if new_user > 20 or new_user < 0:
                    compute_total.pop(user_input)
                    print("Exceeds the prescribed amount!")
                    cishu-1
                    continue
                elif new_user > suijishu1:
                    print("Too big")
                elif new_user == suijishu1:
                    try:
                        last_dict.pop("")
                    except KeyError:
                        pass
                    with open("game_date/"+name+".txt",'a') as f:
                        end = time.time()
                        times = "time cost:%0.2fsecond\n" % (end-start)
                        f.write("Game time:{}\n".format(time.ctime()))
                        print("Guess it！")
                        print(times)
                        f.write(times)
                        a1 = "Guess the'{}'times, this time you guess the total number{}\n".format(cishu,get_num1)
                        print(a1)
                        f.write(a1)
                        if not_reast == set():
                            a2 = "There is no duplication！\n"
                            f.write(a2)
                            f.write("__________________________________________________________________________________\n\n\n")
                            print(a2)
                            break
                        else:
                            for i in zip(last_dict.items(),last_dict.values()):
                                a3 = " num:'{}'\trepeat'{}'Times\n".format(i[0][0],i[1])
                                f.write(a3)
                                print(a3)
                        a4 = "Remove the duplicates, only guess the {} times, only entered{}\n".format(len(set(get_num1)),set(get_num1))
                        f.write(a4)
                        print(a4)
                        f.write("__________________________________________________________________________________\n\n\n")
                        break
                elif new_user < suijishu1:
                    print("Too small")
                cishu+=1
            elif user == "2":
                if new_user > 50 or new_user < 0:
                    compute_total.pop(user_input)
                    print("Exceeds the prescribed amount!")
                    cishu - 1
                    continue
                elif new_user > suijishu2:
                    print("Too big")
                elif new_user == suijishu2:
                    try:
                        last_dict.pop("")
                    except KeyError:
                        pass
                    with open("game_date/" + name + ".txt", 'a') as f:
                        end = time.time()
                        times = "time cost:%0.2fsecond\n" % (end-start)
                        f.write("Game time:{}\n".format(time.ctime()))
                        f.write(times)
                        print("Guess it！")
                        print(times)
                        a1 = "Guess the'{}'times, this time you guess the total number{}\n".format(cishu, get_num2)
                        print(a1)
                        f.write(a1)
                        if not_reast == set():
                            a2 = "There is no duplication！\n"
                            f.write(a2)
                            f.write("__________________________________________________________________________________\n\n\n")
                            print(a2)
                            break
                        else:
                            for i in zip(last_dict.items(), last_dict.values()):
                                a3 = " num:'{}'\trepeat'{}'Times\n".format(i[0][0], i[1])
                                f.write(a3)
                                print(a3)
                        a4 = "Remove the duplicates, only guess the {} times, only entered{}\n".format(len(set(get_num2)), set(get_num2))
                        f.write(a4)
                        print(a4)
                        f.write("__________________________________________________________________________________\n\n\n")
                        break
                elif new_user < suijishu2:
                    print("Too small")
                cishu += 1
            elif user == "3":
                if new_user > 100 or new_user < 0:
                    compute_total.pop(user_input)
                    print("Exceeds the prescribed amount!")
                    cishu - 1
                    continue
                elif new_user > suijishu3:
                    print("Too big")
                elif new_user == suijishu3:
                    try:
                        last_dict.pop("")
                    except KeyError:
                        pass
                    with open("game_date/" + name + ".txt", 'a') as f:
                        end = time.time()
                        times = "time cost:%0.2fsecond\n" % (end-start)
                        f.write("Game time:{}\n".format(time.ctime()))
                        f.write(times)
                        print("Guess it！")
                        print(times)
                        a1 = "Guess the'{}'times, this time you guess the total number{}\n".format(cishu, get_num3)
                        print(a1)
                        f.write(a1)
                        if not_reast == set():
                            a2 = "There is no duplication！\n"
                            f.write(a2)
                            f.write("__________________________________________________________________________________\n\n\n")
                            print(a2)
                            break
                        else:
                            for i in zip(last_dict.items(), last_dict.values()):
                                a3 = " num:'{}'\trepeat'{}'Times\n".format(i[0][0], i[1])
                                f.write(a3)
                                print(a3)
                        a4 = "Remove the duplicates, only guess the {} times, only entered{}\n".format(len(set(get_num3)), set(get_num3))
                        f.write(a4)
                        print(a4)
                        f.write("__________________________________________________________________________________\n\n\n")
                        break
                elif new_user < suijishu3:
                    print("Too small")
                cishu += 1

# 除了超级管理员(root)以外的管理员
def must_root(name):
    print(name)
    with open("user_date.txt",'r') as f:
        root_user = json.load(f)
    with open("user_mail.txt",'r') as m:
        root_mail = json.load(m)
    with open("administrator.txt",'r') as f1:
        root_user2 = json.load(f1)
    print("Admin login is only one chance! Account or password error is directly out")
    while True:
        with open("user_date.txt",'r') as f:
            root_user = json.load(f)
        with open("user_mail.txt",'r') as m:
            root_mail = json.load(m)
        with open("administrator.txt",'r') as f1:
            root_user2 = json.load(f1)
        with open("root.txt",'r') as r:
            roots = json.load(r)
        print("Dear administrator'{}',The menu is as follows:".format(name))
        print("--------------------------")
        print("| 1.delete users         |")
        print("| 2.View all user names  |")
        print("| 3.Not yet developed    |")
        print("| 4.sign out             |")
        print("--------------------------")
        user_selet = input(">>> ")
        if user_selet == "1":
            print("Please enter the user name to be deleted")
            user = input(">>> ")
            if user == name:
                print("Warning! You can not delete yourself！")
                stop()
            elif user in root_user2 or user in roots:
                print("Permission is not enough! You can not delete the administrator'{}'".format(user))
                stop()
            elif user in root_user:
                try:
                    root_user.pop(user)
                    root_mail.pop(user)
                except KeyError:
                    pass
                if os.name == "posix":  # 如果是Linux系统就直接用 'rm' 删除
                    os.system("rm game_date/{}".format(user + ".txt"))
                else:  # 如果是windows系统就用 'os.remove' 删除
                    os.remove("game_date/{}".format(user + ".txt"))
                print("'{}' successfully deleted！".format(user))
                with open("user_date.txt", 'w') as f1:
                    json.dump(root_user, f1)
                with open("user_mail.txt", 'w') as f2:
                    json.dump(root_mail, f2)
                with open("root_date/{}".format(name+".txt"),'a') as r:
                    r.write("\n\n-------------------------------\n")
                    r.write("Time:{} Deleted user'{}'".format(time.ctime(),user))
                    r.write("\n-------------------------------\n")
                stop()
            else:
                print("Sorry, no users found{}".format(user))
                stop()
        elif user_selet == "2":
            for name in root_user:    # 全部的用户名都在"user_date.txt"中
                if name in roots:
                    print("username:{}\tpermissions'{}'".format(name, "Super Administrator"))
                elif name in root_user2 and name not in roots: # 管理员的用户名在"root.txt"中
                    print("username:{}\tpermissions'{}'".format(name, "Administrator"))
                else:
                    print("username:{}\tpermissions'{}".format(name, "Players"))
            stop()
        elif user_selet == "3":
            print("Not yet developed！")
            stop()
        elif user_selet == "4":
            print("Administrator{},Quits!".format(name))
            break
        else:
            print("sorry, we do not have that{}".format(user_selet))
            stop()

def stop():
    print("---------------------------------")
    input("Enter any key to continue!")
    print("----------------------------")
    print("Jump to menu...")
    time.sleep(2)
    print("----------------------------")

# 管理员登录
def Root():
    print("--------------------------")
    print("|  ~Administrator Login~ |")
    print("--------------------------")
    with open("user_date.txt",'r') as f:
        root_user = json.load(f)
    with open("user_mail.txt",'r') as m:
        root_mail = json.load(m)
    with open("administrator.txt",'r') as f1:
        root_user2 = json.load(f1)
    with open("root_mail.txt",'r') as m1:
        root_mail2 = json.load(m1)
    with open("root.txt",'r') as r:
        roots = json.load(r)
    print("Super administrator login is only one chance! Account or password error is directly out")
    root = input("account number: ")
    password = getpass.getpass("Password: ")
    mail = input("Mail: ")
    root_md5 = hasd_md5(root,password)
    try:
        if root in roots and mail == root_mail2[root] and root_md5 == roots[root]:
            print("login successful! Welcome! Super administrator:{}".format(root))
            while True:
                with open("user_date.txt", 'r') as f:
                    root_user = json.load(f)
                with open("user_mail.txt", 'r') as m:
                    root_mail = json.load(m)
                with open("root.txt", 'r') as f1:
                    root_user2 = json.load(f1)
                with open("root_mail.txt", 'r') as m1:
                    root_mail2 = json.load(m1)
                with open("administrator.txt",'r') as ad:
                    ads = json.load(ad)
                print("Dear administrator'{}',The menu is as follows".format(root))
                print("----------------------------------")
                print("| 1.delete users                 |")
                print("| 2.Create a new administrator   |")
                print("| 3.View all users               |")
                print("| 4.View user registration       |")
                print("| 5.sign out                     |")
                print("----------------------------------")
                user_selet = input(">>> ")
                if user_selet == "1":
                    print("Please enter the user name to be deleted")
                    user = input(">>> ")
                    if user == "root":
                        print("caveat! You can not delete yourself!")
                        stop()
                    elif user in root_user and user not in ads:
                        # 删除文本文件中的数据pop()
                        try:
                            root_user.pop(user)
                            root_mail.pop(user)
                        except KeyError:
                            pass
                        # 删除在game_date和root_date中的用户文件
                        if os.name == "posix":      # 如果是Linux系统就直接用 'rm' 删除
                            os.system("rm game_date/{}".format(user+".txt"))
                        else:                       # 如果是windows系统就用 'os.remove' 删除
                            os.remove("game_date/{}".format(user+".txt"))
                        # 把删除掉的数据重新写入
                        with open("user_date.txt",'w') as f1:
                            json.dump(root_user,f1)
                        with open("user_mail.txt",'w') as f2:
                            json.dump(root_mail,f2)
                        with open("root_date/root.txt",'a') as f3:
                            f3.write("\n\n-------------------------------------------------------------------\n")
                            f3.write("time:{}，Deleted user'{}'".format(time.ctime(),user))
                            f3.write("\n-------------------------------------------------------------------\n")
                        print("'{}' successfully deleted！".format(user))
                        stop()
                    elif user in ads:
                        try:
                            root_user.pop(user)
                            ads.pop(user)
                            root_mail2.pop(user)
                        except KeyError:
                            pass
                        if os.name == "posix":
                            os.system("rm game_date/{}".format(user+".txt"))
                            os.system("rm root_date/{}".format(user+".txt"))
                        else:
                            os.remove("game_date/{}".format(user+".txt"))
                            os.remove("root_date/{}".format(user+".txt"))
                        with open("user_date.txt",'w') as f1:
                            json.dump(root_user,f1)
                        with open("administrator.txt",'w') as f3:
                            json.dump(root_user2,f3)
                        with open("root_mail.txt",'w') as f4:
                            json.dump(root_mail2,f4)
                        with open("root_date/{}".format(root+".txt"), 'a') as r:
                            r.write("\n\n-------------------------------\n")
                            r.write("time:{}，Deleted user'{}'".format(time.ctime(), user))
                            r.write("\n-------------------------------\n")
                        print("'{}' successfully deleted！".format(user))
                        stop()
                    else:
                        print("Sorry, no users found'{}'".format(user))
                        stop()
                elif user_selet == "2":
                    with open("administrator.txt", 'r') as u:  # 获取本地文本文件里的用户数据(用户名和密码)
                        root_name = json.load(u)
                    with open("root_mail.txt",'r') as m:  # 同上，获取本地用户的用户名和邮箱(两个都是dict)
                        root_main = json.load(m)
                    with open("user_date.txt",'r') as f:
                        user_name = json.load(f)
                    with open("user_mail.txt",'r') as f:
                        user_mail = json.load(f)
                    while True:
                        print("Enter q to exit the registration")
                        # get_mail = [i for i in root_main.values()]  # 得到邮箱
                        get_user_mail = [x for x in user_mail.values()]
                        new_name = input("root name: ")
                        if new_name == "q" or new_name == "Q":
                            print("Unregistered!")
                            stop()
                            break
                        new_password = getpass.getpass("root Password: ")
                        again_password = getpass.getpass("Again Password:")
                        root_mails = input("Mail: ")
                        password_chack = [i for i in new_password if i.isalpha()]  # 检查密码里面有没有带字母，没有就是[]空list
                        mail_split = root_mails.split("@")  # 将邮箱拆成两半
                        mail_re = re.findall(r'[^a-z0-9]+', mail_split[0])  # 匹配,有数字和字母都ok,其他都不要
                        if len(new_name.split()) != 1 or (new_name.strip() == new_name) == False:
                            print("user name not have strip")
                        elif new_password != again_password:  # 判断两次的密码是否相同
                            print("Twice the password is not the same, please re-enter!")
                            continue
                        elif new_name in root_name and new_name in user_name:  # 检查 新的用户名有没有在本地数据库中
                            print("username already exists！")
                            continue
                        elif len(new_password) <= 6 or password_chack == []:  # 密码长度不能小于6位数，并且至少有一个字母
                            print("Password is too weak. Please enter at least 6 digits and at least 1 letter")
                        elif root_mails in get_user_mail:  # 检查 邮箱有没有被注册
                            print("'%s' The mailbox is already registered！" % root_mails)
                        elif mail_re != [] or mail_split[-1] not in ["qq.com", "gmail.com","163.com"]:  # 检查 用户输入的邮箱格式
                            print("please enter your vaild email")
                        else:
                            get_user_md5 = hasd_md5(new_name, new_password)
                            root_name[new_name] = get_user_md5
                            root_user[new_name] = get_user_md5  # 数据库里面的都是dict
                            root_main[new_name] = root_mails
                            with open("administrator.txt", 'w') as f:
                                json.dump(root_name, f)  # 重新写入本地数据库
                            os.system(r"echo > root_date/{}.txt".format(new_name))  # 在注册成功的同时将用户的Game数据创建了～
                            print("%s Created successfully！" % new_name)
                            with open("root_date/{}".format(root+ ".txt"), 'a') as r:
                                r.write("\n\n-------------------------------\n")
                                r.write("Time:{} Created an administrator'{}'".format(time.ctime(), new_name))
                                r.write("\n-------------------------------\n")
                            with open("root_date/" + new_name + ".txt", 'w') as f:
                                f.write("----------------------------------------------------------------------------\n")
                                f.write("Dear administrator'{}',You are welcome to join us!\n".format(new_name))
                                f.write("Created time:")
                                f.write(time.ctime())
                                f.write("\n---------------------------------------------------------------------------\n\n\n")
                            with open("root_mail.txt", 'w') as s:
                                json.dump(root_main, s)
                            with open("user_date.txt",'w') as f:
                                json.dump(root_user,f)
                            with open("game_date/" + new_name + ".txt", 'w') as f:
                                f.write("----------------------------------------------------------------------------\n")
                                f.write("Dear'{}',You are welcome to join us!\n".format(new_name))
                                f.write("Created time: ")
                                f.write(time.ctime())
                                f.write("\nYou have administrator privileges")
                                f.write("\n---------------------------------------------------------------------------\n\n\n")
                                break
                elif user_selet == "3":
                    with open("user_mail.txt", 'r') as m:
                        mails = json.load(m)
                    with open("root.txt", 'r') as r:
                        spuer = json.load(r)
                    with open("root_mail.txt", 'r') as rm:
                        spuer_mail = json.load(rm)
                    with open("administrator.txt",'r') as admin:
                        admins = json.load(admin)
                    with open("user_date.txt",'r') as user_date:
                        user_dates = json.load(user_date)
                        print("-------------------------------------")
                        print("| 1.View the user name              |")
                        print("| 2.View the user name and mailbox  |")
                        print("-------------------------------------")
                        user = input(">>> ")
                        if user == "1":
                            for name in user_dates:
                                if name in spuer and name not in admins:
                                    print("username:{}\tpermissions'{}'".format(name,"Super Administrator"))
                                elif name in admins and name not in spuer:
                                    print("username:{}\tpermissions'{}'".format(name, "Administrator"))
                                else:
                                    print("username:{}\tpermissions'{}'".format(name, "Players"))
                            stop()
                        elif user == "2":
                            a = [i for i in spuer.keys()]
                            b = [i for i in admins.keys()]
                            # 因为root.txt文件里没有管理员的邮箱，所以要吧root_mail.txt里面的邮箱添加到root.txt中(mails)
                            for i in zip(spuer_mail.keys(), spuer_mail.values()):
                                mails[i[0]] = i[1]
                            for mail in zip(mails.keys(), mails.values()):
                                if mail[0] in a:
                                    print("username:{}\tmail:{}\tpermissions'{}'".format(mail[0], mail[1], "Super Administrator"))
                                elif mail[0] in b:
                                    print("username:{}\tmail:{}\tpermissions'{}'".format(mail[0], mail[1], "Administrator"))
                                else:
                                    print("username:{}\tmail:{}\tpermissions'{}'".format(mail[0], mail[1], "Players"))
                            stop()
                        else:
                            print("sorry, we do not have that{}".format(user))
                            stop()
                elif user_selet == "4":
                    with open("date.txt",'r') as date:
                        if os.name == "posix":
                            os.system("gedit date.txt")
                        else:
                            os.system("date.txt")
                        stop()
                elif user_selet == "5":
                    print("{} Quits！".format(root))
                    break
                else:
                    print("Sorry, no options{}".format(user_selet))
                    stop()
        elif mail != root_mail2[root]:
            print("Mailbox error！")
        elif root in root_user2 and mail == root_mail2[root] and root_md5 == root_user2[root] and root not in roots:
            print("administrator'{}',Welcome！".format(root))
            must_root(root)
        else:
            print("The administrator account or password is incorrect")
    except KeyError:
        print("{}，You are not an administrator！".format(root))

# 用户id
def user_id():
    with open("user_date.txt",'r') as ud:
        user_name = json.load(ud)
    with open("user_id.txt",'r') as uid:
        user_ids = json.load(uid)
    while True:
        suijishu = str(randint(1, 1000))
        if name in user_name and suijishu != user_ids[name] and len(user_ids[name]) == 0:
            user_name[name] = suijishu
            with open("user_id.txt",'w') as f:
                json.dump(user_name,f)
                break
        else:
            break

# 实例运行
if __name__ == "__main__":
    try:
        os.mkdir("game_date")
        open("game_date/root.txt",'w')
        os.mkdir("root_date")
        open("root_date/root.txt",'w')
    except FileExistsError:
        pass
    # 首次运行，要设置一个root账户
    if os.path.exists("user_date.txt") == False and os.path.exists("user_mail.txt") == False and os.path.exists("root.txt") == False and os.path.exists("root_mail.txt") == False and os.path.exists("administrytor.txt") == False: # 判断需要的文件是否都存在
        print("You are using the first time, please enter the root account and password")
        while True:
            name = input("root name: ")
            password = getpass.getpass("root passowrd: ")
            mail = input("root mail: ")
            password_chack = [i for i in password if i.isalpha()]  # 检查密码里面有没有带字母，没有就是[]空list
            mail_split = mail.split("@")  # 将邮箱拆成两半
            mail_re = re.findall(r'[^a-z0-9]+', mail_split[0])  # 匹配,有数字和字母都ok,其他都不要
            if len(name.split()) != 1 or (name.strip() == name) == False:
                print("user name not have strip")
            elif len(password) <= 6 or password_chack == []:  # 密码长度不能小于6位数，并且至少有一个字母
                print("Password is too weak. Please enter at least 6 digits and at least 1 letter")
            elif mail_re != [] or mail_split[-1] not in ["qq.com", "gmail.com", "163.com"]:  # 检查 用户输入的邮箱格式
                print("please enter your vaild email")
            else:
                name_pass = {}
                name_mail = {}
                get_md5 = hasd_md5(name,password)
                name_pass[name] = get_md5
                name_mail[name] = mail
                re_date = (
                           ("root.txt",name_pass),
                           ("root_mail.txt",name_mail))
                for i in re_date:
                    if os.path.exists(i[0]):
                        pass
                    else:
                        with open(i[0],'w') as rd:
                            json.dump(i[1],rd)
                    open("date.txt",'w')
                admins = {}
                with open("user_date.txt",'w') as name_pass:
                    json.dump(admins,name_pass)
                with open("user_mail.txt",'w') as name_mail:
                    json.dump(admins,name_mail)
                with open("administrator.txt",'w') as admin:
                    json.dump(admins,admin)
                break
    if os.path.exists("administrytor.txt") == False and os.path.exists("user_date.txt") == False and os.path.exists("user_mail.txt") == False and os.path.exists("root.txt") == False and os.path.exists("root_mail.txt") == False:
        print("File is missing, please re-run!")
        pass
    else:
        print("Welcome to Guess number Game2.0")
        print("----------------")
        print("| 1.login      |")
        print("| 2.registere  |")
        print("| 3.Root login |")
        print("----------------")
        print("Please login or register before the game starts！")
        start_Game = input("1~2~3 >>> ")
        if start_Game == "1":
            ReL = Register()
            ReL.Login()
        elif start_Game == "2":
            print("REGISTERED!")
            Re = Register()
            if Re.register() == "A":
                # R = Register()
                Re.Login()
        elif start_Game == "3":
            print("Administrator Login")
            Root()
        else:
            print("Sorry, there is no option '%s'" % start_Game)