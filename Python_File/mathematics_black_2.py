# -*- coding: utf-8 -*-

a = input("请输入两位数以上的整数： ")
s = a
while True:
	f = a
	if a == a[::-1]:
		break
	a = str(int(a)+int(a[::-1]))
	print("%s + %s = %s" % (f,f[::-1],a))
print("%s 最后的回数是： %s" % (s,a))