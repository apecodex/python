# -*- conding: utf-8 -*-

from random import randint
"""
def input_count():
	generate_list = []
	reset_repeat = {}
	compute_total = {}
	get_list = []
	while True:
		user_input = int(input(">>>"))
		reset_repeat[user_input]=1
		generate_list.append(user_input)
		s = generate_list.count(user_input)
		compute_total[user_input]=s
		reset_list = [i for i in generate_list if generate_list.count(i) > 1]
		get_num = set(reset_list)
		if user_input == 70:
			L = {}
			for i in get_num:
				f = compute_total.get(i)
				get_list.append(f)
				
				L[i]=get_list[-1]

			if user_input == 70:
				print("此次您输入的数字都有：%s,重复的有: %s,全部重复的只能算一次" % (generate_list,L))
				break
			



	



def Float_number(user_input):
	L = []
	one_num = randint(1,100)
	first_num = randint(1,100)
	last_num = randint(1,100)
	L.append(first_num)
	L.append(last_num)
	float_num = L[0]+L[1]/10*0.1
	if user_input > 100 or user_input < 0:
		raise "must 0`100!"
	if user_input > float_num or user_input > one_num:
		if isinstance(user_input,int):
			print(one_num,"太大了！")
		else:
			print(float_num,"太大了！")
	elif user_input == float_num or user_input == one_num:
		if isinstance(user_input,int):
			print(one_num,"OK!")
			pass
		else:
			print(float_num,"OK!")
			pass
	elif user_input < float_num or user_input < one_num:
		if isinstance(user_input,int):
			print(one_num,"太小啦！")
		else:
			print(float_num,"太小啦！")




while True:
	user_input = input(">>> ")
	randint_int = randint(1,100)
	if user_input.isnumeric():
		user_input = int(user_input)
		Float_number(user_input)
	elif "." in user_input:
		user_input = float(user_input)
		Float_number(user_input)
	else:

		raise "must be a intget!"
"""

generate_list = []      # 用来放用户所输入的所有数
reset_repeat = {}	    # 用来放删除的重复的数
compute_total = {}		# 用来放重复的数
get_list = []			# 获取所有重复的数的个数
cishu = 0
one_num = randint(1,20)			# 生产随机数字

#first_num = randint(1,100)
#last_num = randint(1,100)
#L.append(first_num)
#L.append(last_num)
#float_num = L[0]+L[1]/10*0.1
print("请输入不大于20,不小于0的整数")
while True:
	cishu+=1
	user_input = input(">>>")       # 用户输入
	reset_repeat[user_input]=1
	generate_list.append(user_input)      # 将用户所输入的数字放在 `generate_list` 中
	s = generate_list.count(user_input)   # 获得重复数字的个数
	compute_total[user_input]=s  		  # 获得重复数字的次数放入 `compute_toatl`
	reset_list = [i for i in generate_list if generate_list.count(i) > 1]     # 去掉重复一次以下的
	get_num = set(reset_list)      # 利用set去掉重复的数字
	reset_list_2 = [i for i in generate_list if generate_list.count(i)]
	L = {}
	len_size = len(set(reset_list_2))
	for i in get_num:             # 遍历get_num,将里面的数添加到 `get_list` 
		f = compute_total.get(i)
		get_list.append(f)			
		L[i]=get_list[-1]         # 得到所有数的一次
	if user_input.isnumeric():
		user_input = int(user_input)
		if user_input > 20 or user_input < 0:
			raise "must 0`20!"
		if user_input > one_num:
			if isinstance(user_input,int):
				print("您猜的是 '%s' 太大了！" % (user_input))

		elif user_input == one_num:
			if isinstance(user_input,int):
				print("恭喜您！猜对了！")
				print("共猜测了'%s'次，此次您输入的数字都有：%s,重复的有: %s,全部重复的只能算一次,所以最后只输入了： %s 所以您只猜了%s次" % (cishu,generate_list,L,sorted(set(reset_list_2)),len_size))
				break
		elif user_input < one_num:
			if isinstance(user_input,int):
				print("您猜的是 '%s' 太小啦！" % (user_input))
	else:
		raise "must be a intget!"