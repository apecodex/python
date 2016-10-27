# -*- coding: utf-8 -*-


def huishu():
	i = int(input(">>> "))
	s = list(filter(lambda n:int(str(n)[::-1])==n,range(1,i+100)))

	if i in s:
		f = str(i)
		if len(f) <= 3:
			print(f[:-1],"+",f[len(f)//2:])
		else:
			print(f[:len(f)//2],"+",f[len(f)//2:])
		print(i,"是回数")
	else:
		print(i,"不是回数")


huishu()