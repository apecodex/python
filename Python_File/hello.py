class Student():
	 
	 def __init__(self,name,age):
	 	self.__name = name
	 	self.__age = age
	 	
	 def Bob(self):
	 	print("I'm [%s], I have [%s]" % (self.__name,self.__age))
	 
	 def pr(self):
	 	print(self.__name)


# 1,1,2,3,5,8.......
def daspari():
	L = 0
	a,b=1,1
	while True:
		a,b=b,a+b
		print(L+1,a)

# 杨辉三角
def Rookie():
	L = [1]
	while True:
		L.append(0)
		L[1:] = [L[i] + L[i+1] for i in range(len(L)-1)]
		print(L)

# 字符串转整数	
def Crazy(x):
	return {"0":0,"1":1,"2":2,"3":3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9}[x]

def Sexy(x,y):
	return i * 10 + y
	
	
	
L = Student(input("Name: "),input("Age: "))
L.Bob()
daspari()
Rookie()
print(list(reduce(Sexy,Crazy)))

