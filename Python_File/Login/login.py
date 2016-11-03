# -*- codint: utf-8 -*-

import json
from registered import *
from Find_password import *

		


while True:
	print("User Login!")
	with open("date.txt","r") as f:
		user_date = json.load(f)
		user = str(input("User Name: "))
		password = str(input("Password: "))
		save_md5 = get_md5(user,password)
		if user not in user_date:
			print("用户名: '%s' 不存在，请注册！" % user)
			print("输入'q'退出,输入'a'继续注册")
			sele = str(input("q or a: "))
			if sele == "q":
				print("已退出！")
				break
			print("REGISTERED!")
			register()
		else:
			if user in user_date and user_date[user]==save_md5:
				print("Login success!")
				print("Welcome %s" % user)
				break
			else:
				print("密码或帐号错误，是否需要找回密码？(y/n)")
				enter = str(input(">>> "))
				if enter == "Y" or enter == "y":
					Find_password()
				else:
					continue