# -*- coding: utf-8 -*-

import json
from registered import *

def Find_password():
	with open("find_password_date.txt",'r') as f:
		mail_date = json.load(f)
	with open("date.txt",'r') as d:
		user_date = json.load(d)
		while True:
			user = str(input("User: "))
			mail = str(input("Mail: "))
			if user in mail_date and mail == mail_date[user]:
				while True:
					new_password = str(input("New Password: "))
					enter_password = str(input("Enter Password: "))
					if new_password == enter_password:
						get_new_md5 = get_md5(user,new_password)
						user_date[user]=get_new_md5
						print("密码修改成功！")
						with open("date.txt",'w') as x:
							json.dump(user_date,x)
							break
					else:
						print("两次输入的密码不相同，请重新输入！")
				break
			else:
				print("用户名或错误!")

