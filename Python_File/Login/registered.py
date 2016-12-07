#! /uer/bin/python3.5
# -*- coding: utf-8 -*-


import hashlib,json,re,getpass



def get_md5(user,password):
	md5 = hashlib.md5()
	md5.update((user+password+"The*Sale").encode('utf-8'))
	return md5.hexdigest()


mail_gesi = ["qq.com","gmail.com","163.com"]


def register():
	with open("date.txt",'r') as f:
		user_date = json.load(f)
	with open("find_password_date.txt",'r') as a:
		find_password = json.load(a)
		while True:
			mail_list = [x for x in find_password.values()]    # 获取之前用户输入过的所有邮箱
			user = str(input("New User: "))
			if user == 'q':
				break
			password = getpass.getpass("Password: ")
			password_chack = [i for i in password if i.isalpha()]    # 判断 password 中是否有英文字母
			mail = str(input("Mail: "))
			save_md5 = get_md5(user,password)    # 将用户输入的密码加密
			mail_split = mail.split("@")
			mail_re = re.findall(r"[^a-z0-9]+",mail_split[0])
			if user in user_date:
				print("'%s' 已存在，请重新输入！" % user)
				continue
			elif len(password) < 6 or password_chack == []:    # 判断密码是否大于6个和是否带有英文字母
				print("密码太弱，请输入6位以上的并且至少有一个英文字母")
			elif mail in mail_list:     # 判断有没有被其他用户输入过
				print("此邮箱已注册！")
			elif mail_re != [] or mail_split[-1] not in mail_gesi:   # 判断邮箱格式
				print("请输入正确的邮箱")
				print("输入'q'可退出注册")
			else:
				user_date[user]=save_md5
				find_password[user]=mail
				print("'%s' 创建成功！" % user)
				with open("date.txt",'w') as s:
					json.dump(user_date,s)
				with open("find_password_date.txt",'w') as x:
					json.dump(find_password,x)
				break
		
