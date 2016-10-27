# -*- coding: utf-8 -*-

# changeover str and output
# 逆转字符串并将其输出


def changeover(strs):
	L = []
	for i in strs:
		L.append(i)
	print("".join(L)[::-1])


i = input(">>> ")
changeover(i)