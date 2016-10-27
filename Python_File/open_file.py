# -*- coding: utf-8 -*-

import os

open_name = str(input("请输入所在文件的绝对路径："))

def Open_file(path=os.path.abspath(".")):

	if open_name == "":
		print("当前位置：%s" % path)
	else:
		try:
			file_ = open(open_name,'r')
			print(file_.read())
			print(file_.name)
			file_.close()
		except FileNotFoundError:
			s = open_name.split("/")
			s = s[-1]
			creater_file_ok = str(input("文件没有找到！请确认路径是否正确！是否创建一个名为'{}'的新文件(y/n)".format(s)))
			if creater_file_ok == "y":
				try:
					with open(open_name,'w') as f:
						print(f.write())
				except TypeError:
					print("已经在'%s',创建了文件%s" % (open_name,s))
			else:
				print("已停止")


Open_file()