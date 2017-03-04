# -*- coding: utf-8 -*-

import json
import hashlib
import os
import getpass
from random import randint
import re
import time

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
        print("--------------")
        print("|  ~注册界面~  |")
        print("--------------")
        with open("user_date.txt",'r') as u:   # 获取本地文本文件里的用户数据(用户名和密码)
            user_name = json.load(u)
        with open("user_mail.txt") as m:     # 同上，获取本地用户的用户名和邮箱(两个都是dict)
            user_main = json.load(m)
            while True:
                print("输入q可退出注册")
                get_mail = [i for i in user_main.values()]  # 得到邮箱
                new_name = input("New name: ")
                if new_name == "q" or new_name == "Q":
                    print("已取消注册!")
                    Re = Register()
                    Re.Login()
                    break
                new_password = getpass.getpass("New Password: ")
                again_password = getpass.getpass("Again Password:")
                new_mail = input("Mail: ")
                password_chack = [i for i in new_password if i.isalpha()]   # 检查密码里面有没有带字母，没有就是[]空list
                mail_split = new_mail.split("@")      # 将邮箱拆成两半
                mail_re = re.findall(r'[^a-z0-9]+',mail_split[0])     # 匹配,有数字和字母都ok,其他都不要
                if new_password != again_password:    # 判断两次的密码是否相同
                    print("两次密码不相同,请重新输入!")
                    continue
                elif new_name in user_name:    # 检查 新的用户名有没有在本地数据库中
                    print("用户名已经存在！")
                    continue
                elif len(new_password) <= 6 or password_chack == []:    # 密码长度不能小于6位数，并且至少有一个字母
                    print("密码太弱，请输入6位数以上且至少有1一个字母")
                elif new_mail in get_mail:     # 检查 邮箱有没有被注册
                    print("'%s' 邮箱已被注册！" % new_mail)
                elif mail_re != [] or mail_split[-1] not in ["qq.com","gmail.com","163.com"]:   #检查 用户输入的邮箱格式
                    print("请输入正确的邮箱")
                else:
                    get_user_md5 = hasd_md5(new_name, new_password)
                    user_name[new_name] = get_user_md5  # 数据库里面的都是dict
                    user_main[new_name] = new_mail
                    with open("user_date.txt",'w') as f:
                        json.dump(user_name,f)   # 重新写入本地数据库
                    if os.name == "posix":
                        os.system(r"echo > game_date/{}.txt".format(new_name))   # 在注册成功的同时将用户的Game数据创建了～
                    else:
                        open("game_date/{}.txt".format(new_name),'w')
                    print("%s 创建成功！" % new_name)
                    with open("date.txt",'a') as d:
                        d.write("\n--------------------------------------------------------------------------\n")
                        d.write("北京时间:{} 用户{}加入了这里".format(time.ctime(),new_name))
                        d.write("\n--------------------------------------------------------------------------\n\n")
                    with open("game_date/"+new_name+".txt",'w') as f:
                        f.write("----------------------------------------------------------------------------\n")
                        f.write("亲爱的'{}',欢迎您加入!\n".format(new_name))
                        f.write("注册时间: ")
                        f.write(time.ctime())
                        f.write("\n---------------------------------------------------------------------------\n\n\n")
                    with open("user_mail.txt",'w') as s:
                        json.dump(user_main,s)
                        return "A"     # 这里返回A是为了注册完后可以直接登录
                        break
    # 找回密码
    def Find_password(self):
        print("--------------")
        print("| ～找回密码～ |")
        print("--------------")
        with open("user_mail.txt",'r') as f:
            user_mail = json.load(f)
        with open("user_date.txt",'r') as d:
            user_name = json.load(d)
        with open("root_mail.txt",'r') as rm:
            root_mail = json.load(rm)
        with open("root.txt",'r') as r:
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
                            print("修改成功！")
                            with open("user_date.txt",'w') as n:     # 将新的数据写入数据库
                                json.dump(user_name,n)
                            with open("root.txt",'w') as rs:
                                json.dump(user_name,rs)
                                break
                        else:
                            print("两次密码不相同!")
                    break
                elif name in user_name and mail == user_mail[name]:     # 判断用户名和邮箱和数据库的合不合
                    while True:
                        New_password = getpass.getpass("New Password: ")
                        again_password = getpass.getpass("Again Password: ")
                        get_new_md5 = hasd_md5(name, New_password)     # 得到新的md5值
                        if New_password == again_password:
                            user_name[name] = get_new_md5
                            print("修改成功！")
                            with open("user_date.txt",'w') as n:     # 将新的数据写入数据库
                                json.dump(user_name,n)
                                break
                        else:
                            print("两次密码不相同!")
                    break
                else:
                    print("用户名或邮箱错误")
    # 主函数，登录
    def Login(self):
        print("Login System!")
        print("--------------")
        print("|  ~登录界面~ |")
        print("--------------")
        while True:
            print("任意键继续登录，输入'q'可取消登录")
            s = input(">>> ")
            if s == "q" or s == "Q":
                print("已取消登录")
                break
            with open("user_date.txt",'r') as u:  # 获取用户的数据
                user_date = json.load(u)
                name = input("User name: ")
                password = getpass.getpass("password: ")
                get_password_md5 = hasd_md5(name,password)
                if name not in user_date:
                    print("用户名 %s 不存在！\n 任意键继续注册,'q'退出" % name)
                    seleste = input(">>> ")      # 退出注册！
                    if seleste == "q":
                        print("已退出!")
                        Re = Register()
                        Re.Login()
                        break
                    print("REGISTERED!")     # 除了输入'q'以外的继续注册
                    Re = Register()
                    Re.register()
                else:
                    if name in user_date and user_date[name] == get_password_md5:     # 判断用户输入的密码是否与数据库的相同
                        print("Welcome %s" % name)
                        with open("date.txt",'a') as d:
                            d.write("\n\n************************************************************\n")
                            d.write("北京时间:{},用户'{}'登录游戏".format(time.ctime(),name))
                            d.write("\n************************************************************\n")
                        print("亲爱的'%s',欢迎您！" % name)
                        while True:
                            print("------------------")
                            print("-------菜单栏------")
                            print("| 1.开始新游戏     |")
                            print("| 2.查看历史记录   |")
                            print("| 3.退出登录       |")
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
                                print("{}，已退出登录!".format(name))
                                with open("date.txt",'a') as f:
                                    f.write("\n\nXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n")
                                    f.write("北京时间:{},用户'{}'退出了登录!".format(time.ctime(),name))
                                    f.write("\nXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n")
                                break
                            else:
                                print("抱歉，选项中没有 '%s'" % user_input)
                                break
                            break
                    else:
                        print("帐号或密码错误，是否找回密码？(y/n)")
                        enter = str(input(">>> "))
                        if enter == "Y" or enter == "y":    #如果密码错误，可选择找回密码（重新设置）
                            print("找回密码")
                            Ref = Register()
                            Ref.Find_password()
                        else:
                            continue

# 游戏
class Game_date:

    def main(self,name):
        print("Start Game!")
        print("----------------")
        print("|   ~游戏界面~   |")
        print("----------------")
        print("请输入不大于20,不小于0的整数")
        cishu = 1
        generate_list = []    # 存储用户输入的每一个数字
        compute_total = {}    # 存储用户输入的重复数字，比如 2 输入了两次就是{"2"：2}
        suijishu1 = randint(0,20)   # 获取随机数
        suijishu2 = randint(0,50)
        suijishu3 = randint(0,100)
        last_dict = {}    # 存储最后重复过的总数,比如 2 最后所输入的6次,就是{"2":6}
        get_list = []     # 得到输入的次数
        print("选择难度: ")
        print("````````````````")
        print("| 1.简单        |")
        print("| 2.一般        |")
        print("| 3.困难        |")
        print("````````````````")
        while True:
            user = input(">>> ")
            if user == "1":
                print("~~~~~简单模式~~~~~")
                with open("date.txt",'a') as d1:
                    d1.write("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
                    d1.write("time:{}\n".format(time.ctime()))
                    d1.write("用户'{}',进行 {} 的游戏".format(name,"简单模式"))
                    d1.write("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
                break
            elif user == "2":
                print("~~~~~一般模式~~~~~")
                with open("date.txt", 'a') as d2:
                    d2.write("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
                    d2.write("time:{}\n".format(time.ctime()))
                    d2.write("用户'{}',进行 {} 的游戏".format(name, "一般模式"))
                    d2.write("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
                    break
            elif user == "3":
                print("~~~~~困难模式~~~~~")
                with open("date.txt",'a') as d3:
                    d3.write("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
                    d3.write("time:{}\n".format(time.ctime()))
                    d3.write("用户'{}',进行 {} 的游戏".format(name,"困难模式"))
                    d3.write("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
                break
            else:
                print("抱歉，没有{}".format(user))
                continue
        print("Are you readr?")
        input("任意开始游戏！")
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
                print("请输入整数")
                cishu-1
                continue
            if user == "1":
                if new_user > 20 or new_user < 0:
                    compute_total.pop(user_input)
                    print("超过规定数额!")
                    cishu-1
                    continue
                elif new_user > suijishu1:
                    print("太大了")
                elif new_user == suijishu1:
                    try:
                        last_dict.pop("")
                    except KeyError:
                        pass
                    with open("game_date/"+name+".txt",'a') as f:
                        end = time.time()
                        times = "共用时%0.2f秒\n" % (end-start)
                        f.write("Game time:{}\n".format(time.ctime()))
                        print("猜对了！")
                        print(times)
                        f.write(times)
                        a1 = "共猜了'{}'次，此次您猜的数字共有'{}\n".format(cishu,get_num1)
                        print(a1)
                        f.write(a1)
                        if not_reast == set():
                            a2 = "没有重复的！\n"
                            f.write(a2)
                            f.write("__________________________________________________________________________________\n\n\n")
                            print(a2)
                            break
                        else:
                            for i in zip(last_dict.items(),last_dict.values()):
                                a3 = " num:'{}'\t重复'{}'次\n".format(i[0][0],i[1])
                                f.write(a3)
                                print(a3)
                        a4 = "去掉重复的，只算猜了{}次,只输入了{}\n".format(len(set(get_num1)),set(get_num1))
                        f.write(a4)
                        print(a4)
                        f.write("__________________________________________________________________________________\n\n\n")
                        break
                elif new_user < suijishu1:
                    print("太小了")
                cishu+=1
            elif user == "2":
                if new_user > 50 or new_user < 0:
                    compute_total.pop(user_input)
                    print("超过规定数额!")
                    cishu - 1
                    continue
                elif new_user > suijishu2:
                    print("太大了")
                elif new_user == suijishu2:
                    try:
                        last_dict.pop("")
                    except KeyError:
                        pass
                    with open("game_date/" + name + ".txt", 'a') as f:
                        end = time.time()
                        times = "共用时%0.2f秒\n" % (end-start)
                        f.write("Game time:{}\n".format(time.ctime()))
                        f.write(times)
                        print("猜对了！")
                        print(times)
                        a1 = "共猜了'{}'次，此次您猜的数字共有'{}\n".format(cishu, get_num2)
                        print(a1)
                        f.write(a1)
                        if not_reast == set():
                            a2 = "没有重复的！\n"
                            f.write(a2)
                            f.write("__________________________________________________________________________________\n\n\n")
                            print(a2)
                            break
                        else:
                            for i in zip(last_dict.items(), last_dict.values()):
                                a3 = " num:'{}'\t重复'{}'次\n".format(i[0][0], i[1])
                                f.write(a3)
                                print(a3)
                        a4 = "去掉重复的，只算猜了{}次,只输入了{}\n".format(len(set(get_num2)), set(get_num2))
                        f.write(a4)
                        print(a4)
                        f.write("__________________________________________________________________________________\n\n\n")
                        break
                elif new_user < suijishu2:
                    print("太小了")
                cishu += 1
            elif user == "3":
                if new_user > 100 or new_user < 0:
                    compute_total.pop(user_input)
                    print("超过规定数额!")
                    cishu - 1
                    continue
                elif new_user > suijishu3:
                    print("太大了")
                elif new_user == suijishu3:
                    try:
                        last_dict.pop("")
                    except KeyError:
                        pass
                    with open("game_date/" + name + ".txt", 'a') as f:
                        end = time.time()
                        times = "共用时%0.2f秒\n" % (end-start)
                        f.write("Game time:{}\n".format(time.ctime()))
                        f.write(times)
                        print("猜对了！")
                        print(times)
                        a1 = "共猜了'{}'次，此次您猜的数字共有'{}\n".format(cishu, get_num3)
                        print(a1)
                        f.write(a1)
                        if not_reast == set():
                            a2 = "没有重复的！\n"
                            f.write(a2)
                            f.write("__________________________________________________________________________________\n\n\n")
                            print(a2)
                            break
                        else:
                            for i in zip(last_dict.items(), last_dict.values()):
                                a3 = " num:'{}'\t重复'{}'次\n".format(i[0][0], i[1])
                                f.write(a3)
                                print(a3)
                        a4 = "去掉重复的，只算猜了{}次,只输入了{}\n".format(len(set(get_num3)), set(get_num3))
                        f.write(a4)
                        print(a4)
                        f.write("__________________________________________________________________________________\n\n\n")
                        break
                elif new_user < suijishu3:
                    print("太小了")
                cishu += 1

# 除了超级管理员(root)以外的管理员
def must_root(name):
    with open("user_date.txt",'r') as f:
        root_user = json.load(f)
    with open("user_mail.txt",'r') as m:
        root_mail = json.load(m)
    with open("root.txt",'r') as f1:
        root_user2 = json.load(f1)
        print("管理员登录只有一次机会！帐号或密码错误则直接退出")
        while True:
            with open("user_date.txt",'r') as f:
                root_user = json.load(f)
            with open("user_mail.txt",'r') as m:
                root_mail = json.load(m)
            with open("root.txt",'r') as f1:
                root_user2 = json.load(f1)
            print("亲爱的管理员'{}',菜单如下:".format(name))
            print("--------------------")
            print("| 1.删除用户         |")
            print("| 2.查看所有用户名    |")
            print("| 3.暂未开发         |")
            print("| 4.退出登录")
            print("--------------------")
            user_selet = input(">>> ")
            if user_selet == "1":
                print("请输入需要删除的用户名")
                user = input(">>> ")
                if user == name:
                    print("警告! 您无法将自己删除！")
                    stop()
                elif user in root_user2:
                    print("权限不够！您无法删除管理员的{}".format(user))
                    time.sleep(0.5)
                    print("----------------------------")
                    print("正在跳转至菜单...")
                    time.sleep(2)
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
                    print("'{}' 删除成功！".format(user))
                    with open("user_date.txt", 'w') as f1:
                        json.dump(root_user, f1)
                    with open("user_mail.txt", 'w') as f2:
                        json.dump(root_mail, f2)
                    with open("root_date/{}".format(name+".txt"),'a') as r:
                        r.write("\n\n-------------------------------\n")
                        r.write("于北京时间:{} 删除了用户'{}'".format(time.ctime(),user))
                        r.write("\n-------------------------------\n")
                    stop()
                else:
                    print("抱歉，没有找到用户{}".format(user))
                    stop()
            elif user_selet == "2":
                for name in root_user:    # 全部的用户名都在"user_date.txt"中
                    if name == "root":
                        print("用户名:{}\t所属权限'{}'".format(name, "超级管理员"))
                    elif name in root_user2: # 管理员的用户名在"root.txt"中
                        print("用户名:{}\t所属权限'{}'".format(name, "管理员"))
                    else:
                        print("用户名:{}\t所属权限'{}".format(name, "普通玩家"))
                stop()
            elif user_selet == "3":
                print("暂未开发！")
                stop()
            elif user_selet == "4":
                print("管理员{},已退出!".format(name))
                break
            else:
                print("抱歉，没有{}".format(user_selet))
                stop()

def stop():
    print("---------------------------------")
    input("输入任意键继续!")
    print("----------------------------")
    print("正在跳转至菜单...")
    time.sleep(2)
    print("----------------------------")

# 管理员登录
def Root():
    print("----------------")
    print("|  ~管理员登录～ |")
    print("----------------")
    with open("user_date.txt",'r') as f:
        root_user = json.load(f)
    with open("user_mail.txt",'r') as m:
        root_mail = json.load(m)
    with open("root.txt",'r') as f1:
        root_user2 = json.load(f1)
    with open("root_mail.txt",'r') as m1:
        root_mail2 = json.load(m1)
    print("超级管理员登录只有一次机会！帐号或密码错误则直接退出")
    root = input("帐号: ")
    password = getpass.getpass("密码: ")
    mail = input("邮箱: ")
    root_md5 = hasd_md5(root,password)
    try:
        if root == "root" and mail == root_mail2[root] and root_md5 == root_user2[root]:
            print("登录成功！欢迎您! 超级管理员:{}".format(root))
            while True:
                with open("user_date.txt",'r') as f:
                    root_user = json.load(f)
                with open("user_mail.txt",'r') as m:
                    root_mail = json.load(m)
                with open("root.txt",'r') as f1:
                    root_user2 = json.load(f1)
                with open("root_mail.txt",'r') as m1:
                    root_mail2 = json.load(m1)
                print("亲爱的{},菜单如下".format(root))
                print("--------------------")
                print("| 1.删除用户        |")
                print("| 2.创建新的管理员   |")
                print("| 3.查看所有用户     |")
                print("| 4.查看用户注册情况 |")
                print("| 5.退出登录        |")
                print("--------------------")
                user_selet = input(">>> ")
                if user_selet == "1":
                    print("请输入需要删除的用户名")
                    user = input(">>> ")
                    if user == "root":
                        print("警告！您无法将自己删除！")
                        stop()
                    elif user in root_user and user not in root_user2:
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
                            f3.write("于北京时间:{}，删除了用户'{}'".format(time.ctime(),user))
                            f3.write("\n-------------------------------------------------------------------\n")
                        print("'{}' 删除成功！".format(user))
                        stop()
                    elif user in root_user2:
                        try:
                            root_user.pop(user)
                            root_user2.pop(user)
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
                        with open("root.txt",'w') as f3:
                            json.dump(root_user2,f3)
                        with open("root_mail.txt",'w') as f4:
                            json.dump(root_mail2,f4)
                        with open("root_date/{}".format(root+".txt"), 'a') as r:
                            r.write("\n\n-------------------------------\n")
                            r.write("于北京时间:{} 删除了用户'{}'".format(time.ctime(), user))
                            r.write("\n-------------------------------\n")
                        print("'{}' 删除成功！".format(user))
                        stop()
                    else:
                        print("抱歉，没有找到用户'{}'".format(user))
                        stop()
                elif user_selet == "2":
                    with open("root.txt", 'r') as u:  # 获取本地文本文件里的用户数据(用户名和密码)
                        root_name = json.load(u)
                    with open("root_mail.txt",'r') as m:  # 同上，获取本地用户的用户名和邮箱(两个都是dict)
                        root_main = json.load(m)
                    with open("user_date.txt",'r') as f:
                        user_name = json.load(f)
                    with open("user_mail.txt",'r') as f:
                        user_mail = json.load(f)
                    while True:
                        print("输入q可退出注册")
                        get_mail = [i for i in root_main.values()]  # 得到邮箱
                        new_name = input("root name: ")
                        if new_name == "q" or new_name == "Q":
                            print("已取消注册!")
                            stop()
                            break
                        new_password = getpass.getpass("root Password: ")
                        again_password = getpass.getpass("Again Password:")
                        root_mails = input("Mail: ")
                        password_chack = [i for i in new_password if i.isalpha()]  # 检查密码里面有没有带字母，没有就是[]空list
                        mail_split = root_mails.split("@")  # 将邮箱拆成两半
                        mail_re = re.findall(r'[^a-z0-9]+', mail_split[0])  # 匹配,有数字和字母都ok,其他都不要
                        if new_password != again_password:  # 判断两次的密码是否相同
                            print("两次密码不相同,请重新输入!")
                            continue
                        elif new_name in root_name and new_name in user_name:  # 检查 新的用户名有没有在本地数据库中
                            print("用户名已经存在！")
                            continue
                        elif len(new_password) <= 6 or password_chack == []:  # 密码长度不能小于6位数，并且至少有一个字母
                            print("密码太弱，请输入6位数以上且至少有1一个字母")
                        elif root_mails in get_mail and root_mail2 in user_mail:  # 检查 邮箱有没有被注册
                            print("'%s' 邮箱已被注册！" % root_mails)
                        elif mail_re != [] or mail_split[-1] not in ["qq.com", "gmail.com","163.com"]:  # 检查 用户输入的邮箱格式
                            print("请输入正确的邮箱")
                        else:
                            get_user_md5 = hasd_md5(new_name, new_password)
                            root_name[new_name] = get_user_md5
                            root_user[new_name] = get_user_md5  # 数据库里面的都是dict
                            root_main[new_name] = root_mails
                            with open("root.txt", 'w') as f:
                                json.dump(root_name, f)  # 重新写入本地数据库
                            os.system(r"echo > root_date/{}.txt".format(new_name))  # 在注册成功的同时将用户的Game数据创建了～
                            print("%s 创建成功！" % new_name)
                            with open("root_date/{}".format(root+ ".txt"), 'a') as r:
                                r.write("\n\n-------------------------------\n")
                                r.write("于北京时间:{} 创建了管理员'{}'".format(time.ctime(), new_name))
                                r.write("\n-------------------------------\n")
                            with open("root_date/" + new_name + ".txt", 'w') as f:
                                f.write("----------------------------------------------------------------------------\n")
                                f.write("亲爱的管理员'{}',欢迎您加入!\n".format(new_name))
                                f.write("创建时间: ")
                                f.write(time.ctime())
                                f.write("\n---------------------------------------------------------------------------\n\n\n")
                            with open("root_mail.txt", 'w') as s:
                                json.dump(root_main, s)
                            with open("user_date.txt",'w') as f:
                                json.dump(root_user,f)
                            with open("game_date/" + new_name + ".txt", 'w') as f:
                                f.write("----------------------------------------------------------------------------\n")
                                f.write("亲爱的'{}',欢迎您加入!\n".format(new_name))
                                f.write("创建时间: ")
                                f.write(time.ctime())
                                f.write("\n您拥有管理员权限")
                                f.write("\n---------------------------------------------------------------------------\n\n\n")
                                break
                elif user_selet == "3":
                    with open("user_mail.txt", 'r') as m:
                        mails = json.load(m)
                    with open("root.txt", 'r') as r:
                        spuer = json.load(r)
                    with open("root_mail.txt", 'r') as rm:
                        spuer_mail = json.load(rm)
                    with open("user_date.txt",'r') as user_date:
                        user_dates = json.load(user_date)
                        print("-----------------------")
                        print("| 1.查看用户名          |")
                        print("| 2.查看用户名和邮箱     |")
                        print("-----------------------")
                        user = input(">>> ")
                        if user == "1":
                            for name in user_dates:
                                if name == "root":
                                    print("用户名:{}\t所属权限'{}'".format(name,"超级管理员"))
                                elif name in spuer:
                                    print("用户名:{}\t所属权限'{}'".format(name, "管理员"))
                                else:
                                    print("用户名:{}\t所属权限'{}'".format(name, "普通玩家"))
                            stop()
                        elif user == "2":
                            a = [i for i in spuer.keys()]
                            # 因为root.txt文件里没有管理员的邮箱，所以要吧root_mail.txt里面的邮箱添加到root.txt中(mails)
                            for i in zip(spuer_mail.keys(), spuer_mail.values()):
                                mails[i[0]] = i[1]
                            for mail in zip(mails.keys(), mails.values()):
                                if mail[0] == "root":
                                    print("用户名:{}\t邮箱:{}\t所属权限'{}'".format(mail[0], mail[1], "超级管理员"))
                                elif mail[0] in a:
                                    print("用户名:{}\t邮箱:{}\t所属权限'{}'".format(mail[0], mail[1], "管理员"))
                                else:
                                    print("用户名:{}\t邮箱:{}\t所属权限'{}'".format(mail[0], mail[1], "普通玩家"))
                            stop()
                        else:
                            print("抱歉，没有{}".format(user))
                            stop()
                elif user_selet == "4":
                    with open("date.txt",'r') as date:
                        if os.name == "posix":
                            os.system("gedit date.txt")
                        else:
                            os.system("date.txt")
                        stop()
                elif user_selet == "5":
                    print("{} 已退出！".format(root))
                    break
                else:
                    print("抱歉，没有选项{}".format(user_selet))
                    stop()
        elif mail != root_mail2[root]:
            print("邮箱错误！")
        elif root in root_user2 and mail == root_mail2[root] and root_md5 == root_user2[root]:
            print("管理员'{}',欢迎您！".format(root))
            must_root(root)
        else:
            print("管理员帐号或密码错误")
    except KeyError:
        print("{}，您不是管理员！".format(root))


if __name__ == "__main__":
    print("Welcome to Guess number Game2.0")
    print("----------------")
    print("| 1.login      |")
    print("| 2.registere  |")
    print("| 3.Root login |")
    print("----------------")
    print("游戏开始前请登录或者注册！")
    try:
        os.mkdir("game_date")
        open("game_date/root.txt",'w')
        os.mkdir("root_date")
        open("root_date/root.txt",'w')
    except FileExistsError:
        pass
    start_Game = input("1~2~3 ")
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
        print("管理员登录")
        Root()
    else:
        print("抱歉，选项中没有 '%s'" % start_Game)
