import requests
from bs4 import BeautifulSoup
import urllib.request
import json
import time
import numpy
import matplotlib.pyplot as plt

headers={"User-Agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36"}
proxies = {'http':'http://27.185.194.55:8118'}
# url = "https://music.163.com/api/v3/playlist/detail?id=161193280"
# a=requests.get(url,headers=headers,proxies=proxies)
# gettext = a.text
# json_url = json.loads(gettext)
# Li = []
# for i in range(len(json_url['playlist']['trackIds'])):
# 	time.sleep(numpy.random.random())
# 	b = "https://music.163.com/api/v1/resource/comments/R_SO_4_{}?".format(json_url['playlist']['trackIds'][i]['id'])
# 	c=requests.get(b,headers=headers,proxies=proxies)
# 	json_url2 = json.loads(c.text)
# 	Li.append(int(json_url2['total']))
# 	print(int(json_url2['total']))
u = "https://music.163.com/api/v1/resource/comments/R_SO_4_25787222"
a=requests.get(u,headers=headers,proxies=proxies)
gettext = a.text
json_url = json.loads(gettext)
# for i in 
for i in range(len(json_url['hotComments'])):
	time.sleep(numpy.random.random())
	print(json_url['hotComments'][i]['content'])
for x in range(len(json_url['comments'])):
	time.sleep(numpy.random.random())
	print(json_url['comments'][i]['content'])

# index = numpy.arange(len(json_url['playlist']['trackIds']))

# pl = plt.bar(left=index,height=Li)
# plt.show()