# -*- coding: utf-8 -*-


def compute_add(x):
	print("写程序输入一个数n并打印出从1到n的和。")
	sum = 0

	for i in range(x):
		sum = sum +1
		print(sum)
		


def beishu(x):
	print("修改上个程序,使得求和的数只包含3或5的倍数,例如n=17,则求和的数为:3, 5, 6, 9, 10, 12, 15")
	for i in range(x):
		if i % 3 == 0 or i % 5 == 0:
			if i >= 3:
				print(i)

def compute_add_or_chenji(x):
	print("写个程序,要求用户输入一个数n,并概率性的选择是计算1到n的和还是计算1到n的乘积。")
	sum = 0
	if x 
