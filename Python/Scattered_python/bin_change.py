# -*- coding: utf-8 -*-

i = 3

a = 2
s= 0
L = []

while i > s:
	L.append(i)
	i = i // 2
print(L)

for x in L:
	print(x,x%2)