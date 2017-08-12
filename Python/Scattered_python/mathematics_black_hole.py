# -*- coding: utf-8 -*-

from functools import reduce

x = str(input("请输入四位数或者三位数的数字： "))
times = 1
while True:
	if len(x) > 4:
		print("不能超过4位数")
		break 

	max_math = sorted(x,reverse=True)
	min_math = sorted(x)
	max_math_switch_str = int(reduce(lambda x,y:x+y,max_math))
	min_math_switch_str = int(reduce(lambda x,y:x+y,min_math))

	s = max_math_switch_str-min_math_switch_str
	print("now",times,max_math_switch_str,"-",min_math_switch_str,"=",s)

	if s == 6174:
		break
	if s == 495:
		break

	x = str(s)
	times += 1