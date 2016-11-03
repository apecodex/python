import string
f = string.punctuation
x = [i for i in f]
a = "1534das.d64dsa"
d = ["123456.","qq.com"]
c = [x for x in d[0]]
if x in c:
	print("!!!!!")
else:
	print("@@@")