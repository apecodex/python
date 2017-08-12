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

from functools import reduce
def compute_add_or_chenji(x):

	print("写个程序,要求用户输入一个数n,并概率性的选择是计算1到n的和还是计算1到n的乘积。")
	sum = 0
	user_seleter = input("乘法还是加法？(*/+): ")

	if user_seleter == "*":
		L = []
		for i in range(1,x):
			L.append(i)
			s = reduce(lambda x,y:x*y,L)
			if s > x:
				break
			else:
				print(s)

	elif user_seleter == "+":
		for i in range(x):
			sum = sum + 1
			print(sum)
	else:
		print("只能算加法或者乘法！")
		pass






def chengfabiao():
	for i in range(1,13):
		for x in range(1,i+1):
			print(i,"*",x,"=",i*x,end=' ')
		print(" ")

def _not_divisible(n):
    return lambda x: x % n > 0
def sushu(n):

	for i in range(2,n-1):
		if n % 2 != 0:
			print(i)
			
			
			
from math import sqrt
N = 1000
list = [p for p in range(2,N) if 0 not in [p % d for d in range(2,int(sqrt(p)) + 1)]]


#print(list)

def _odd_iter():
    n = 1
    while True:
        n = n + 2
        print(n)

#_odd_iter()
def _not_divisible(n):
    return lambda x: x % n > 0

def primes():
    yield 2
    it = _odd_iter() # 初始序列
    while True:
        n = next(it) # 返回序列的第一个数
        yield n
        it = filter(_not_divisible(n), it)



"""
for n in primes():
    if n < 1000:
        print(n)
    else:
        break
"""
import math
def is_prime(n):                                            
    list_num = []    
    for i in range(2, n):        
        for num in range(2, int(math.sqrt(n))+1):            
            if i % num == 0 and i != num:             
                break          
            elif i % num != 0 and num == int(math.sqrt(n)):
            	list_num.append(i) 
    print(list_num)  



