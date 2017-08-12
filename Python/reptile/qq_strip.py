import requests
import json
import numpy
import time


cookie = ""   # 输入自己的 cookie
header = {
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
'Connection': 'keep-alive',
'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Cookie': cookie}
proxies = {'http':'http://27.185.194.55:8118'}
times = 0
while True:
	print("第 {} 页".format(((times//10)+1)))
	print("----------------------------------------")
	url = "https://h5.qzone.qq.com/proxy/domain/m.qzone.qq.com/cgi-bin/new/get_msgb?uin=1473018671&hostUin=1473018671&num=10&start={}&hostword=0&essence=1&s={}&iNotice=0&inCharset=utf-8&outCharset=utf-8&format=jsonp&ref=qzone&g_tk=159637896&qzonetoken=2a26403b960220332f267c6736eec1e4053e1f6eb5791eb2fe314429eb084741d2f4b70466ac0e7f1c".format(str(times),numpy.random.random())
	# url地址要自己去开发者工具里面拿~上面的这个是我自己的~复制自己的修改一下就行了~
	regs = requests.get(url, proxies=proxies, headers=header)
	str_qiepian = regs.text[10:-3]
	js = json.loads(str_qiepian)['data']['commentList']
	if js == []:
		print("Over! 共计 {} 页".format(json.loads(str_qiepian)['data']['total']))
		break
	else:
		for page in range(len(js)):
			print("第{}页的第{}条 留言者:{} \t 内容:{}".format((times//10)+1,page+1,js[page]['nickname'],js[page]['ubbContent']))
	times+=10
	time.sleep(numpy.random.random())
