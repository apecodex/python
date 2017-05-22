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

    CREATE TABLE players_data(
    id INTEGER UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id INTEGER UNSIGNED,
    game_time DATETIME,
    second CHAR(32),
    guess_times CHAR(32),
    total_input VARCHAR(255),
    repetition VARCHAR(12),
    mode VARCHAR(32),
    FOREIGN KEY (user_id) REFERENCES user (id)
    );
    CREATE TABLE login_exit_time(
    id INTEGER UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id INTEGER UNSIGNED,
    login_time DATETIME,
    exit_time DATETIME,
    FOREIGN KEY (user_id) REFERENCES user (id)
    );
    CREATE TABLE del_user(
    id INTEGER UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    admin_id INTEGER UNSIGNED,
    remove_user_name VARCHAR(88),
    FOREIGN KEY (admin_id) REFERENCES administrator (id)
    )
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
        get_max_id = self.cursor.execute("SELECT MAX(id) FROM user;")
        for i in get_max_id:
            ids.append(i[0])
        data = """
        INSERT INTO user (id,name,password,mail,`time`) VALUES ({},'{}','{}','{}','{}');
        """.format(ids[0]+1,name,password,mail,self.get_time())
        get_message_max_id = self.cursor.execute("SELECT MAX(id) FROM players_data;")
        for m in get_message_max_id:
            message_id.append(m[0])
        date_message = """
        INSERT INTO players_data (id,user_id,game_time,second,total_input,repetition,mode) VALUES ({},{},'{}',{},'{}','{}','{}');
        """.format(message_id[0]+1,ids[0]+1,'0000-00-00-00-00',0,'','','No')
        self.cursor.execute(data)
        self.cursor.execute(date_message)
        self.cursor.close()
        self.connect_sql.commit()
        self.connect_sql.close()

    #添加管理员数据
    def add_admin(self,name,password,mail):
        user_id = []
        admin_id = []
        get_user_max_id = self.cursor.execute("SELECT * FROM user WHERE id=(SELECT MAX(id) from user);")
        for i in get_user_max_id:
            user_id.append(i[0])
        get_admin_max_id = self.cursor.execute("SELECT * FROM administrator WHERE id=(SELECT MAX(id) from administrator);")
        for i in get_admin_max_id:
            admin_id.append(i[0])
        data = """
        INSERT INTO user (id,name,password,mail,'time') VALUES ({},'{}','{}','{}','{}');
        """.format(user_id[0]+1,name,password,mail,self.get_time())
        admin_data = """
        INSERT INTO administrator (id,user_id,create_time) VALUES ({},{},'{}');
        """.format(admin_id[0]+1,user_id[0]+1,self.get_time())
        self.cursor.execute(data)
        self.cursor.execute(admin_data)
        self.cursor.close()
        self.connect_sql.commit()
        self.connect_sql.close()

    # 存储用户的游戏数据
    def players_data(self,name,game_time,second,total_input,repetition,mode):
        message_id = []
        find_uid = """
        SELECT id FROM players_data WHERE user_id=(SELECT id FROM user WHERE name='{}');
        """.format(name)
        players_message_id = self.cursor.execute(find_uid)
        get_max_id = self.cursor.execute("SELECT MAX(id) FROM players_message;")
        for m in get_max_id:
            message_id.append(m[0])
        save_data = """
        INSERT INTO players_data (id,user_id,game_time,second,total_input,repetition,mode) VALUES ({},{},'{}',{},'{}','{}','{}')
        """.format(message_id[0],players_message_id,game_time,second,total_input,repetition,mode)
        self.cursor.execute(save_data)
        self.cursor.close()
        self.connect_sql.commit()
        self.connect_sql.close()


    #删除用户（ROOT）
    def root_pop_sql(self,name):
        del_id = []
        get_max_id = self.cursor.execute("SELECT MAX(id) FROM del_id;")
        for m in get_max_id:
            del_id.append(m[0])
        delete_user = "DELETE FROM user WHERE id=(SELECT id FROM user WHERE name='{}')".format(name)
        delete_admin = "DELETE FROM administrator WHERE user_id=(SELECT id FROM user WHERE name='{}')".format(name)
        delete_players_data = "DELETE FROM players_data WHERE user_id=(SELECT id FROM user WHERE name='{}')".format(name)
        delete_date_recard = "INSERT INTO del_user (id,admin_id,remove_user_name) VALUES ({},{},'{}')".format(del_id[0],1,name)
        self.cursor.execute(delete_user)
        self.cursor.execute(delete_admin)
        self.cursor.execute(delete_players_data)
        self.cursor.execute(delete_date_recard)
        self.cursor.close()
        self.connect_sql.commit()
        self.connect_sql.close()

    #删除用户 (administrator)
    def admin_pop_sql(self,name):
        remove_user = "DELETE FROM user WHERE id=(SELECT id FROM user WHERE name='{}')".format(name)
        remove_palyers_data = "DELETE FROM players_data WHERE user_id=(SELECT id FROM user WHERE name='{}')".format(name)
        self.cursor.execute(remove_user)
        self.cursor.execute(remove_palyers_data)
    
    #找回密码
    def find_passworld(self,name,new_password):
        get_user_date = "UPDATE user SET password = '{}' WHERE id=(SELECT id FROM user WHERE name='{}')".format(new_password,name)
        self.cursor.execute(get_user_date)
        self.cursor.close()
        self.connect_sql.commit()
        self.connect_sql.close()

# 加密密码
def hasd_md5(user,password):
    md5 = hashlib.md5()
    md5.update((user+password+"Guess*Number").encode())
    return md5.hexdigest()


# 登录系统
class Register:

    # 初始化
    def __init__(self):
        self.connect_sql = sqlite3.connect('guess_number.db')
        self.cursor = self.connect_sql.cursor()

    # 注册
    def register(self):
        print("------------------------------")
        print("|  ~Registration interface~  |")
        print("------------------------------")
        while True:
            print("Enter q to exit the registration")
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
            check_name_list = []
            check_name = self.cursor.execute("SELECT name FROM user WHERE name='{}';".format(new_name))
            for names in check_name:
                check_name_list.append(names)
            check_mail_list = []
            check_mail = self.cursor.execute("SELECT mail FROM user WHERE mail='{}';".format(new_mail))
            for mails in check_mail:
                check_mail_list.append(mails)
            if len(new_name.split()) != 1 or (new_name.strip() == new_name) == False:  # 用户名中不能有空格
                print("user name not have strip")
            elif new_password != again_password:    # 判断两次的密码是否相同
                print("Twice the password is not the same, please re-enter!")
                continue
            elif check_name_list != []:    # 检查 新的用户名有没有在本地数据库中
                print("username '{}' already exists!".format(new_name))
                continue
            elif len(new_password) <= 6 or password_chack == []:    # 密码长度不能小于6位数，并且至少有一个字母
                print("Password is too weak. Please enter at least 6 digits and at least 1 letter")
            elif check_mail_list != []:     # 检查 邮箱有没有被注册
                print("'%s' The mailbox is already registered!" % new_mail)
            elif mail_re != [] or mail_split[-1] not in ["qq.com","gmail.com","163.com"]:   #检查 用户输入的邮箱格式对不对
                print("please enter your vaild email")
            else:
                get_user_md5 = hasd_md5(new_name, new_password)
                O = Options_sql()
                O.add_sql(new_name,get_user_md5,new_mail)
                print("%s Created successfully！" % new_name)  # 创建成功！
                return "A"     # 这里返回A是为了注册完后可以直接登录
                break

    # 找回密码
    def Find_password(self):
        print("------------------------")
        print("| ～Find the password～ |")
        print("------------------------")
        while True:
            name = input("user name: ")
            mail = input("Mail: ")
            name_mail_date = []
            get_name_mail = "SELECT name,mail FROM user WHERE name='{}'".format(name)
            for lc in self.cursor.execute(get_name_mail):
                name_mail_date.append(lc)
            check_name_list = []
            check_name = self.cursor.execute("SELECT name FROM user WHERE name='{}';".format(name))
            for names in check_name:
                check_name_list.append(names)
            print(name_mail_date)
            print(check_name_list)
            if check_name_list == []:    # 检查 新的用户名有没有在本地数据库中
                print("username '{}' already exists!".format(name))
                continue
            elif name == name_mail_date[0][0] and mail == name_mail_date[0][1]:
                New_password = getpass.getpass("New Password: ")
                again_password = getpass.getpass("Again Password: ")
                get_new_md5 = hasd_md5(name, New_password)     # 得到新的md5值
                password_chack = [i for i in New_password if i.isalpha()]   # 检查密码里面有没有带字母，没有就是[]空list
                if New_password != again_password:    # 判断两次的密码是否相同
                    print("Twice the password is not the same, please re-enter!")
                    continue
                elif len(New_password) <= 6 or password_chack == []:    # 密码长度不能小于6位数，并且至少有一个字母
                    print("Password is too weak. Please enter at least 6 digits and at least 1 letter")
                    continue
                elif New_password == again_password:
                    O = Options_sql()
                    O.find_passworld(name,get_new_md5)
                    print("Successfully modified！")
                    break
                else:
                    print("The password is not the same twice!")
            else:
                print("User name %s does not exist or mailbox error" % (name))

    # 主函数，登录
    def Login(self):
        print("Login System!")
        print("----------------------")
        print("|  ~Login Interface~ |")
        print("----------------------")
        total_user = {}
        try:
            select_user_data = self.cursor.execute("SELECT name,password FROM user;")
        except sqlite3.ProgrammingError:
            pass
        for check in select_user_data:
            total_user[check[0]] = check[1]
        while True:
            print("Any key to continue to log in, enter 'q' to cancel the login")
            s = input(">>> ")
            if s == "q" or s == "Q":
                print("Sign-in canceled")
                break
            name = input("User name: ")
            password = getpass.getpass("password: ")
            get_password_md5 = hasd_md5(name,password)
            if name == "" and password == "":
                print("Account or password cannot be empty!")
            elif name not in total_user:
                print("User name %s does not exist! \nAny key to continue registration, 'q' to exit" % name)
                seleste = input(">>> ")     
                if seleste == "q":
                    print("Quits!")
                    Re = Register()
                    Re.Login()
                    break
                print("REGISTERED!")
                Re = Register()
                Re.register()
            else:
                if name in total_user and get_password_md5 == total_user[name]:
                    O = Options_sql()
                    login_times = O.get_time()
                    print("Dear'%s',Welcome!" % name)
                    while True:
                        print("------------------")
                        print("-------Menu Bar--------")
                        print("| 1.Start a new game  |")
                        print("| 2.View history      |")
                        print("| 3.sign out          |")
                        print("-----------------------")
                        user_input = input("1-2-3 ")
                        if user_input == "1":
                            game = Game_date()
                            game.main(name)
                            stop()
                            continue
                        elif user_input == "2":
                            find_sql = "SELECT game_time,second,guess_times,total_input,repetition,mode FROM players_data WHERE user_id=(SELECT id FROM user WHERE name='{}');".format(name)
                            select_palyers_data = self.cursor.execute(find_sql)
                            for date in select_palyers_data:
                                if date[4] == "0":    
                                    print('Game Times: %s\n' % date[0])
                                    print("Game Mode: %s\n" % date[5])
                                    print("You guess the '%s' times,the number enteren is '%s'\n" % (date[2],"".join(date[3])))
                                    print("There is no duplication！\n")
                                    print("use times: %s\n" % date[1])
                                    print("-------------------------------------------------------\n")
                                elif date[4] == "1":
                                    print('Game Times: %s\n' % date[0])
                                    print("Game Mode: %s\n" % date[5])
                                    print("You guess the '%s' times,the number enteren is '%s'\n" % (date[2],"".join(date[3])))
                                    get_reast = date[3].split(',')
                                    get_exceed_two = [i for i in get_reast if get_reast.count(i) >= 2]
                                    exceed_list = {}
                                    for i in set(get_exceed_two):
                                        exceed_list[i] = get_exceed_two.count(i)
                                    for exceed in zip(exceed_list.items(),exceed_list.values()):
                                        print("num:'{}'\trepeat'{}'Times\n".format(exceed[0][0],exceed[1]))
                                    get_reast = "".join(date[3]).split(',')
                                    filter_reast = set(get_reast)
                                    print("According to the requirements, not repeat, remove duplicate, you only guess '%s' times,The end result is '%s'" % (len(set(date[3].split(","))),",".join(filter_reast)))
                                    print("use times: %s\n" % date[1])
                                    print("-------------------------------------------------------\n")
                                else:
                                    print("You haven't played")
                            stop()
                            continue
                        elif user_input == "3":
                            ids = []
                            get_login_exit_max_id = self.cursor.execute("SELECT MAX(id) FROM login_exit_time;")
                            for i in get_login_exit_max_id:
                                ids.append(i[0])
                            select_user_str = "SELECT id FROM user WHERE name='{}';".format(name)
                            get_user_id = self.cursor.execute(select_user_str)
                            name_id = []
                            for x in get_user_id:
                                name_id.append(x[0])
                            exit_times = O.get_time()
                            select_times = "INSERT INTO login_exit_time (id,user_id,login_time,exit_time) VALUES ({},{},'{}','{}')".format(ids[0]+1,name_id[0],login_times,exit_times)
                            save_exit_time = self.cursor.execute(select_times)
                            print("{},exit".format(name))
                            self.cursor.close()
                            self.connect_sql.commit()
                            self.connect_sql.close()
                            break
                        else:
                            print("Sorry, no option '%s' " % user_input)
                            continue
                        break
                else:
                    print("Account or password mistake, back?(y/n)")
                    enter = str(input(">>> "))
                    if enter == "Y" or enter == "y":  
                        print("Find the password")
                        Ref = Register()
                        Ref.Find_password()
                        break
                    else:
                        continue
# 游戏
class Game_date:

    def __init__(self):
        self.connect_sql = sqlite3.connect("guess_number.db")
        self.cursor = self.connect_sql.cursor()

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
        O = Options_sql()
        get_times = O.get_time()
        while True:
            user = input(">>> ")
            if user == "1":
                print("~~~~~Simple mode~~~~~")
                print("Please enter an integer no greater than 20 and no less than 0")
                break
            elif user == "2":
                print("~~~~~General Mode~~~~~")
                print("Please enter an integer no greater than 50 and no less than 0")
                break
            elif user == "3":
                print("~~~~~Difficult mode~~~~~")
                print("Please enter an integer no greater than 100 and no less than 0")
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
                        end = time.time()
                        times = "time cost:%0.2fsecond\n" % (end-start)
                        print("Guess it！")
                        print(times)
                        print("Guess the'{}'times, this time you guess the total number {}\n".format(cishu,",".join(get_num1)))
                        times2 = "%0.2f" % (end-start)
                        ids = []
                        get_palyers_data_max_id = self.cursor.execute("SELECT MAX(id) FROM players_data")
                        for i in get_palyers_data_max_id:
                            ids.append(i[0])
                        user_id_str = "SELECT id FROM user WHERE name='{}'".format(name)
                        get_user_id = self.cursor.execute(user_id_str)
                        for i in get_user_id:
                            ids.append(i[0])
                        not_reast_sql_save_zero = "INSERT INTO players_data (id,user_id,game_time,second,guess_times,total_input,repetition,mode) VALUES ({},{},'{}',{},{},'{}','{}','{}')".format(ids[0]+1,ids[1],get_times,float(times2),cishu,",".join(get_num1),'0',"simple")
                        not_reast_sql_save_one = "INSERT INTO players_data (id,user_id,game_time,second,guess_times,total_input,repetition,mode) VALUES ({},{},'{}',{},{},'{}','{}','{}')".format(ids[0]+1,ids[1],get_times,float(times2),cishu,",".join(get_num1),'1',"simple")
                        ax = [i for i in get_num1 if get_num1.count(i) >= 2]
                        if ax == []:
                            self.cursor.execute(not_reast_sql_save_zero)
                            print("There is no duplication！\n")
                        else:
                            for i in zip(last_dict.items(),last_dict.values()):
                                a3 = " num:'{}'\trepeat'{}'Times\n".format(i[0][0],i[1])
                                print(a3)
                            self.cursor.execute(not_reast_sql_save_one)
                            print("Remove the duplicates, only guess the {} times, only entered{}\n".format(len(set(get_num1)),set(get_num1)))
                        self.cursor.close()
                        self.connect_sql.commit()
                        self.connect_sql.close()
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
                        end = time.time()
                        times = "time cost:%0.2fsecond\n" % (end-start)
                        print("Guess it！")
                        print(times)
                        print("Guess the'{}'times, this time you guess the total number {}\n".format(cishu,",".join(get_num2)))
                        times2 = "%0.2f" % (end-start)
                        ids = []
                        get_palyers_data_max_id = self.cursor.execute("SELECT MAX(id) FROM players_data")
                        for i in get_palyers_data_max_id:
                            ids.append(i[0])
                        user_id_str = "SELECT id FROM user WHERE name='{}'".format(name)
                        get_user_id = self.cursor.execute(user_id_str)
                        for i in get_user_id:
                            ids.append(i[0])
                        not_reast_sql_save_zero = "INSERT INTO players_data (id,user_id,game_time,second,guess_times,total_input,repetition,mode) VALUES ({},{},'{}',{},{},'{}','{}','{}')".format(ids[0]+1,ids[1],get_times,float(times2),cishu,",".join(get_num2),'0',"general")
                        not_reast_sql_save_one = "INSERT INTO players_data (id,user_id,game_time,second,guess_times,total_input,repetition,mode) VALUES ({},{},'{}',{},{},'{}','{}','{}')".format(ids[0]+1,ids[1],get_times,float(times2),cishu,",".join(get_num2),'1',"general")
                        ax = [i for i in get_num2 if get_num2.count(i) >= 2]
                        if ax == []:
                            self.cursor.execute(not_reast_sql_save_zero)
                            print("There is no duplication！\n")
                        else:
                            for i in zip(last_dict.items(),last_dict.values()):
                                a3 = " num:'{}'\trepeat'{}'Times\n".format(i[0][0],i[1])
                                print(a3)
                            self.cursor.execute(not_reast_sql_save_one)
                            print("Remove the duplicates, only guess the {} times, only entered{}\n".format(len(set(get_num2)),set(get_num2)))
                        self.cursor.close()
                        self.connect_sql.commit()
                        self.connect_sql.close()
                        break
                elif new_user < suijishu3:
                    print("Too small")
                cishu+=1
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
                        end = time.time()
                        times = "time cost:%0.2fsecond\n" % (end-start)
                        print("Guess it！")
                        print(times)
                        print("Guess the'{}'times, this time you guess the total number {}\n".format(cishu,",".join(get_num3)))
                        times2 = "%0.2f" % (end-start)
                        ids = []
                        get_palyers_data_max_id = self.cursor.execute("SELECT MAX(id) FROM players_data")
                        for i in get_palyers_data_max_id:
                            ids.append(i[0])
                        user_id_str = "SELECT id FROM user WHERE name='{}'".format(name)
                        get_user_id = self.cursor.execute(user_id_str)
                        for i in get_user_id:
                            ids.append(i[0])
                        not_reast_sql_save_zero = "INSERT INTO players_data (id,user_id,game_time,second,guess_times,total_input,repetition,mode) VALUES ({},{},'{}',{},{},'{}','{}','{}')".format(ids[0]+1,ids[1],get_times,float(times2),cishu,",".join(get_num3),'0',"difficult")
                        not_reast_sql_save_one = "INSERT INTO players_data (id,user_id,game_time,second,guess_times,total_input,repetition,mode) VALUES ({},{},'{}',{},{},'{}','{}','{}')".format(ids[0]+1,ids[1],get_times,float(times2),cishu,",".join(get_num3),'1',"difficult")
                        ax = [i for i in get_num3 if get_num3.count(i) >= 2]
                        if ax == []:
                            self.cursor.execute(not_reast_sql_save_zero)
                            print("There is no duplication！\n")
                        else:
                            for i in zip(last_dict.items(),last_dict.values()):
                                a3 = " num:'{}'\trepeat'{}'Times\n".format(i[0][0],i[1])
                                print(a3)
                            self.cursor.execute(not_reast_sql_save_one)
                            print("Remove the duplicates, only guess the {} times, only entered{}\n".format(len(set(get_num3)),set(get_num3)))
                        self.cursor.close()
                        self.connect_sql.commit()
                        self.connect_sql.close()
                        break
                elif new_user < suijishu3:
                    print("Too small")
                cishu+=1

# 除了超级管理员(root)以外的管理员
def must_root(name):
    connect_sql = sqlite3.connect("guess_number.db")
    cursor = connect_sql.cursor()
    print("Admin login is only one chance! Account or password error is directly out")
    while True:
        print("Dear administrator'{}',The menu is as follows:".format(name))
        print("--------------------------")
        print("| 1.delete users         |")
        print("| 2.View all user names  |")
        print("| 3.Not yet developed    |")
        print("| 4.sign out             |")
        print("--------------------------")
        user_selet = input(">>> ")
        if user_selet == "1":
            print("暂未开发....(其实是不知道怎么办了.....)")
            stop()
            continue
            admin_id = []
            not_list = []
            for ids in cursor.execute("SELECT user_id FROM administrator"):
                admin_id.append(ids[0])
            print("Please enter the user name to be deleted")
            user = input(">>> ")

            # user_name_select = "SELECT user_id FROM administrator WHERE user_id=(SELECT id FROM user WHERE name='{}');".format(user)
            # for i in [i[0] for i in cursor.execute(user_name_select)]:
            #     not_list.append(i)
            # print(admin_id,not_list)
            # if user == name:
            #     print("Warning! You can not delete yourself！")
            #     stop()
            # elif not_list[0] in admin_id:
            #     print("Permission is not enough! You can not delete the administrator'{}'".format(user))
            #     stop()
            # elif not_list[0] not in admin_id:
            #     print("!!!")
            #     # O = Options_sql()
            #     # O.admin_pop_sql(user)
            #     # stop()
            # else:
            #     print("Sorry, no users found {}".format(user))
            #     stop()
        elif user_selet == "2":
            admin_id = []
            for aid in cursor.execute("SELECT user_id FROM administrator;"):
                admin_id.append(aid[0])
            get_name_sql = "SELECT id,name FROM user;"
            for name in cursor.execute(get_name_sql):
                if name[0] == 1:
                    print("username:{}\tpermissions'{}'".format(name[1],"Super Administrator"))
                elif name[0] in admin_id:
                    print("username:{}\tpermissions'{}'".format(name[1], "Administrator"))
                else:
                    if name[0] not in admin_id:
                        print("username:{}\tpermissions'{}'".format(name[1], "Players"))
            stop()
        elif user_selet == "3":
            print("Not yet developed！")
            stop()
        elif user_selet == "4":
            print("Administrator *{}*,Quits!".format(name[1]))
            break
        else:
            print("sorry, we do not have that '{}'".format(name))
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
    connect_sql = sqlite3.connect('guess_number.db')
    cursor = connect_sql.cursor()
    print("--------------------------")
    print("|  ~Administrator Login~ |")
    print("--------------------------")
    first_name = []
    get_name_one = cursor.execute('SELECT * FROM user WHERE id=1')
    for name in get_name_one:
        first_name.append(name)
    print("Super administrator login is only one chance! Account or password error is directly out")
    root = input("account number: ")
    password = getpass.getpass("Password: ")
    mail = input("Mail: ")
    root_md5 = hasd_md5(root,password)
    try:
        get_admin_id = []
        admin_date = []
        administrator_id = "SELECT user_id FROM administrator WHERE user_id=(SELECT id FROM user WHERE name='{}');".format(root)
        for admin_id in cursor.execute(administrator_id):
            get_admin_id.append(admin_id[0])
        if get_admin_id == []:
            pass
        else:
            get_admin_date = 'SELECT name,password,mail FROM user WHERE id={};'.format(get_admin_id[0])
            for x in cursor.execute(get_admin_date):
                admin_date.append(x)
    except IndexError:
        pass

    if root == first_name[0][1] and root_md5 == first_name[0][2] and mail == first_name[0][3]:
        print("login successful! Welcome! Super administrator:{}".format(root))
        while True:
            print("Dear administrator'{}',The menu is as follows".format(root))
            print("----------------------------------")
            print("| 1.delete users                 |")
            print("| 2.Create a new administrator   |")
            print("| 3.View all users               |")
            print("| 4.View user registration       |")
            print("| 5.View user login exit         |")
            print("| 6.sign out                     |")
            print("----------------------------------")
            user_selet = input(">>> ")
            if user_selet == "1":
                print("Please enter the user name to be deleted")
                user = input(">>> ")
                first_id = []
                name = []
                get_user_total_date = "SELECT name FROM user WHERE id=1;"
                for dates in cursor.execute(get_user_total_date):
                    first_id.append(dates[0])
                get_name = "SELECT name FROM user WHERE name='{}'".format(user)
                for n in cursor.execute(get_name):
                    name.append(n[0])
                if user == first_id[0]:
                    print("caveat! You can not delete yourself!")
                    stop()
                elif name != []:
                    O = Options_sql()
                    O.root_pop_sql(user)
                    print("'{}' successfully deleted！".format(user))
                    stop()
                else:
                    print("Sorry, no users found '{}'".format(user))
                    stop()
            elif user_selet == "2":
                while True:
                    print("Enter q to exit the registration")
                    # get_mail = [i for i in root_main.values()]  # 得到邮箱
                    # get_user_mail = [x for x in user_mail.values()]
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
                    check_name_list = []
                    check_name = cursor.execute("SELECT name FROM user WHERE name='{}';".format(new_name))
                    for names in check_name:
                        check_name_list.append(names)
                    check_mail_list = []
                    check_mail = cursor.execute("SELECT mail FROM user WHERE mail='{}';".format(root_mails))
                    for mails in check_mail:
                        check_mail_list.append(mails)
                    if len(new_name.split()) != 1 or (new_name.strip() == new_name) == False:
                        print("user name not have strip")
                    elif new_password != again_password:  # 判断两次的密码是否相同
                        print("Twice the password is not the same, please re-enter!")
                        continue
                    elif check_name_list != []:  # 检查 新的用户名有没有在本地数据库中
                        print("username '{}' already exists！".format(new_name))
                        continue
                    elif len(new_password) <= 6 or password_chack == []:  # 密码长度不能小于6位数，并且至少有一个字母
                        print("Password is too weak. Please enter at least 6 digits and at least 1 letter")
                    elif check_mail_list != []:  # 检查 邮箱有没有被注册
                        print("'%s' The mailbox is already registered！" % root_mails)
                    elif mail_re != [] or mail_split[-1] not in ["qq.com", "gmail.com","163.com"]:  # 检查 用户输入的邮箱格式
                        print("please enter your vaild email")
                    else:
                        get_user_md5 = hasd_md5(new_name, new_password)
                        print("%s Created successfully！" % new_name)
                        O = Options_sql()
                        O.add_admin(new_name,get_user_md5,root_mails)
                        break
            elif user_selet == "3":
                    print("-------------------------------------")
                    print("| 1.View the user name              |")
                    print("| 2.View the user name and mailbox  |")
                    print("-------------------------------------")
                    user = input(">>> ")
                    if user == "1":
                        admin_id = []
                        for aid in cursor.execute("SELECT user_id FROM administrator;"):
                            admin_id.append(aid[0])
                        get_name_sql = "SELECT id,name FROM user;"
                        for name in cursor.execute(get_name_sql):
                            if name[0] == 1:
                                print("username:{}\tpermissions'{}'".format(name[1],"Super Administrator"))
                            elif name[0] in admin_id:
                                print("username:{}\tpermissions'{}'".format(name[1], "Administrator"))
                            else:
                                if name[0] not in admin_id:
                                    print("username:{}\tpermissions'{}'".format(name[1], "Players"))
                        stop()
                    elif user == "2":
                        admin_id = []
                        for aid in cursor.execute("SELECT user_id FROM administrator;"):
                            admin_id.append(aid[0])
                        get_name_sql = "SELECT id,name,mail FROM user;"
                        for name in cursor.execute(get_name_sql):
                            if name[0] == 1:
                                print("username:{}\tmail:{}\tpermissions'{}'".format(name[1], name[2], "Super Administrator"))
                            elif name[0] in admin_id:
                                print("username:{}\tmail:{}\tpermissions'{}'".format(name[1], name[2], "Administrator"))
                            else:
                                if name[0] not in admin_id:
                                    print("username:{}\tmail:{}\tpermissions'{}'".format(name[1], name[2], "Players"))
                        stop()
                    else:
                        print("sorry, we do not have that{}".format(user))
                        stop()
            elif user_selet == "4":
                for dates in cursor.execute("SELECT name,`time` FROM user WHERE id!=1"):
                    times = dates[1].split("-")
                    times_add = times[0]+" year "+times[1]+" month "+times[2]+" day "+times[3]+":"+times[4]+":"+times[5]
                    print("user: *{}*\ttime:{} Join to here!,".format(dates[0],times_add))
                stop()
            elif user_selet == "5":
                # for le in cursor.execute("SELECT ")
                print("Sorry~~暂未开发!")
            elif user_selet == "6":
                print("{} Quits！".format(root))
                break
            else:
                print("Sorry, no options{}".format(user_selet))
                stop()
    elif root == first_name[0][1] and root_md5 == first_name[0][2] and mail != first_name[0][3]:
        print("Mailbox error！")
    elif root == admin_date[0][0] and root_md5 == admin_date[0][1] and mail == admin_date[0][2]:
        print("administrator'{}',Welcome！".format(root))
        must_root(root)
    elif root == first_name[0][1] and root_md5 != first_name[0][2] or root != first_name[0][1] and root_md5 == first_name[0][2]:
        print("The administrator account or password is incorrect")
    else:
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
    if os.path.exists("guess_number.db"):
        pass
    else:
        sql_db()
    # 首次运行，要设置一个root账户
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
                get_md5 = hasd_md5(name,password)
                admins = {}
                O = Options_sql()
                connect_sql = sqlite3.connect("guess_number.db")
                cursor = connect_sql.cursor()
                FIRST_DATA = "INSERT INTO user (id,name,password,mail,`time`) VALUES ({},'{}','{}','{}','{}');".format(1,name,get_md5,mail,O.get_time())
                PALYERS_DATA = "INSERT INTO players_data (id,user_id,game_time,second,guess_times,total_input,repetition,mode) VALUES ({},{},'{}',{},{},'{}','{}','{}');".format(1,1,'0000-00-00-00-00',0,0,'','','No')
                ADMINISTRATOR_DATA = "INSERT INTO administrator (id,user_id,create_time) VALUES ({},{},'{}')".format(1,1,O.get_time())
                LOGIN_EXIT_TIME_DATA = "INSERT INTO login_exit_time (id,user_id,login_time,exit_time) VALUES (1,1,'0000-00-00-00-00','0000-00-00-00-00')"
                DEL_USER = "INSERT INTO del_user (id,admin_id,remove_user_name) VALUES (1,1,"")"
                cursor.execute(FIRST_DATA)
                cursor.execute(PALYERS_DATA)
                cursor.execute(ADMINISTRATOR_DATA)
                cursor.execute(LOGIN_EXIT_TIME_DATA)
                cursor.execute(DEL_USER)
                cursor.close()
                connect_sql.commit()
                connect_sql.close()
                break

    if os.path.exists("guess_number.db") == False:
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
