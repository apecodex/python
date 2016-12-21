# -*- coding: utf-8 -*-

import requests,json
from bs4 import BeautifulSoup
import os
from urllib import request,parse


headers = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}

url = "http://www.ishadowsocks.net/"

r = request.urlopen(url)
s = r.read().decode("utf-8")

rs = BeautifulSoup(s,'lxml')

L = []
rss = rs.find("section",id="free").find_all("h4")
for i in rss[:18]:
	ps = i.get_text().replace("：",":")
	end = ps.split(':')[1]
	L.append(end)
a = L[:4]
b = L[6:10]
c = L[12:16]
print(a,'\n',b,'\n',c,'\n',end=' ')