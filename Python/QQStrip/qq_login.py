import requests
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities,ActionChains
from selenium.common.exceptions import NoSuchElementException,WebDriverException
import time
from bs4 import BeautifulSoup
import re
import pickle
from urllib import request
import json
from datetime import datetime
import threading
import pymysql
import base64

class Sql():

	# 输入数据库的账号和密码
	# 账号一般默认是root,不是的话请更改
	def __init__(self,root='root',password=''):
		self.connect_sql = pymysql.connect(user=root, password=password, host="127.0.0.1", port=3306)
		self.connect_cursor = self.connect_sql.cursor()
		self.connect_cursor.execute("CREATE DATABASE IF NOT EXISTS qqstrip DEFAULT CHARACTER SET utf8;")
		self.connect_sql.commit()
		self.connect_cursor.execute("USE qqstrip;")

	def sql(self):
		data = """
		CREATE TABLE IF NOT EXISTS qqnumber(
		qq_friends VARCHAR(30),
		qq_number VARCHAR(30),
		shuoshuokey VARCHAR(88)
		);
		"""
		self.connect_cursor.execute(data)
		self.connect_sql.commit()

	def save(self,qq_friends,qq_number,shuoshuokey):
		self.sql()
		data = """
		INSERT INTO qqnumber (qq_friends,qq_number,shuoshuokey) VALUES ('{}','{}','{}');
		""".format(qq_friends,qq_number,shuoshuokey)
		self.connect_cursor.execute(data)
		self.connect_sql.commit()


class qzone_login():

	def __init__(self,username="",password="",sqlroot='',sqlpassword=''):
		self.username= username
		self.password = password
		self.headers = {
			"user-agent": "Mozilla/5.0 (Linux; U; Android 2.3.6; zh-cn; GT-S5660 Build/GINGERBREAD) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1 MicroMessenger/4.5.255"}
		dcap = dict(DesiredCapabilities.PHANTOMJS)
		dcap["phantomjs.page.settings.userAgent"] = (
			"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
			'*/*',
			'en-US,en;q=0.8',
			'max-age=0',
			'keep-alive'

		)
		self.browser = webdriver.PhantomJS(executable_path=r"phantomjs-2.1.1-windows\bin\phantomjs.exe",desired_capabilities=dcap)
		self.browser.set_window_size(480,500)
		self.browser.get("https://mobile.qzone.qq.com")
		try:
			self.sql = Sql(sqlroot, sqlpassword)
		except pymysql.err.OperationalError:
			print("数据库账号或者密码错误!")
			root = input("数据库账号: ")
			password = input("数据库密码: ")
			self.sql = Sql(root,password)
		print("Start!")

	def save_screens(self):
		self.browser.get('https://mobile.qzone.qq.com')
		self.browser.save_screenshot('ceshi5.png')

	# 需要验证
	# 1.打开手机QQ安全中心，查看动态验证码
	# 2.使用短信验证(暂时未搞~)
	def fuck_verify_code(self):
		Bs = BeautifulSoup(self.browser.page_source,'lxml')
		# print(self.browser.page_source)
		try:
			try:
				Bfind = Bs.find('iframe')['src']    # 获取动态验证码的页面url
				self.browser.get(Bfind)
			except TypeError:
				print("这个验证码可能会出现无法获取的情况,请关闭程序重启运行，会尽快解决！！！Sorry~")
		except WebDriverException:
			print("这个验证码可能会出现无法获取的情况,请关闭程序重启运行，会尽快解决！！！Sorry~")
			# self.reboot_verify_code()
		time.sleep(2)
		token_code = self.browser.find_element_by_xpath('//*[@id="token_code"]')
		btn = self.browser.find_element_by_xpath('//*[@id="scroller"]/div[2]/form/div[1]/button')
		verify_code = input("动态验证码: ")    # 输入动态码
		verify_code_action = ActionChains(self.browser)
		verify_code_action.move_to_element(token_code).click().send_keys(verify_code)
		verify_code_action.move_to_element(btn).click()
		verify_code_action.perform()
		time.sleep(5)
		self.browser.save_screenshot('ceshi4.png')
		print("登陆成功!,正在保存cookie....")
		cookie = {}
		for c in self.browser.get_cookies():
			cookie[c['name']] = c['value']
		self.sava_cookie(self.username,cookie)
		print("正在爬取!")
		uin = self.get_fristdotai_time(self.get_sid(self.browser.page_source))['loginuin']
		qzonetoken = self.get_qzonetoken(self.getCookie(self.username))
		gtk = self.get_gtk(self.getCookie(self.username))
		firstrtime = self.get_fristdotai_time(self.get_sid(self.browser.page_source))['times']
		self.get_dotai_sad(uin,qzonetoken,gtk,firstrtime)
		print("OVER")
	#  识别图标的验证
	def reboot_verify_code(self):
		time.sleep(3)
		url = "https://ssl.captcha.qq.com/cap_union_new_show?aid=549000929&captype=&protocol=https&clientype=1&disturblevel=&apptype=2&noheader=0&color=&showtype=&fb=1&theme=&lang=2052&sess=BNMDwCNY6DHgvp19N75V1T62mdLntiP-PmMrPsSDfhljYM3PbvQa2YmZAiRB5yNaTGAJmEgshmGdugfAHEFElzFJsj25whcKd4PAMeNWF2tFbbPmPSMJ-zwovyzlm4D_WeopGav24sgESs1e47uDuSMicJPnaDpkbs3QCquiF2BmVEfgz-nW19mJEIEHdJxYn1XQd-wkyCU*&fwidth=0&uid=1473018671&cap_cd=-2wDJk7I9ogP7glTeXWzGfZ9pzEC6vuCa9cSAkbUMizVwgdtBrq8xA**&rnd=339939"
		# BS = BeautifulSoup(url,'lxml')
		# Bfind = BS.find('iframe')['src']
		# self.browser.get(Bfind)
		self.browser.get(url)
		cap_input = self.browser.find_element_by_xpath('//*[@id="cap_input"]')
		cap_que_img = self.browser.find_element_by_xpath('//*[@id="cap_que_img"]')
		verify_btn = self.browser.find_element_by_xpath('//*[@id="verify_btn"]')
		self.dowload_verify_code_img(cap_que_img)
		verify_code_input = input("验证码: ")
		action_code = ActionChains(self.browser)
		cap_input.clear()
		action_code.move_to_element(cap_input).click().send_keys(verify_code_input)
		action_code.move_to_element(verify_btn).click()
		action_code.perform()

	def dowload_verify_code_img(self,element):
		print("正在下载验证码图片....")
		url = element.get_attribute('src')
		fileName = element.get_attribute('id') + '.jpg'
		request.urlretrieve(url,fileName)
		print("下载完成，正在打开~")

	def sava_cookie(self,qq,cookies):
		file = open('{}.txt'.format(qq),'wb')
		json_pickle = pickle.dump(cookies,file)
		file.close()

	def getCookie(self,qq):
		try:
			with open("{}.txt".format(qq),'rb') as f:
				cookie = pickle.load(f)
			return cookie
		except EOFError:
			pass

	def setCookie(self,qq):
		with open('{}.txt'.format(qq),'rb') as f:
			cookies = pickle.load(f)
			f.close()
			try:
				for cookie in cookies:
					self.browser.add_cookie(cookie)
			except Exception as e:
				print(e)
				print(self.browser.title)

	# 获取qzonetoken
	def get_qzonetoken(self,cookie):
		url = "https://user.qzone.qq.com/" + self.username
		headers = {
			"user-agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"}
		request_url = requests.get(url, headers=headers, cookies=cookie).text
		BS = BeautifulSoup(request_url, 'lxml')
		Bfind = BS.find_all('script', type="text/javascript")[-1]
		pattern = re.compile(r'{ try{return ".*?";}')
		for br in Bfind:
			return pattern.findall(br)[0].split(" ")[2][1:-3]

	# 生成g_tk
	def get_gtk(self,cookie):
		hashes = 5381
		for g in cookie['p_skey']:
			hashes += (hashes << 5) + ord(g)
		return hashes & 0x7fffffff

	# 获取sid
	def get_sid(self,text):
		Bs = BeautifulSoup(text,'lxml')
		bfind = Bs.find_all("script",type="application/javascript")
		pattern = re.compile(r'window.g_App = {"sid":".*?",')
		for i in bfind[1]:
			return pattern.findall(i)[0].split(':')[1][1:-2]

	# 获取说说浏览量
	# 如果需要设置输出时间~就更改starttime和stoptime参数,默认输出全部
	# 出来starttime和stoptime参数,其余参数请默认！
	def get_sad_see(self,uin=None,appid=None,logid=None,gtk=None,qzonetoken=None,starttime=None,stoptime=None):
		url = "https://h5.qzone.qq.com/proxy/domain/g.qzone.qq.com/cgi-bin/friendshow/cgi_get_visitor_single?uin={}&appid={}&blogid={}&param={}&ref=qzfeeds&beginNum=1&num=24&g_tk={}&qzonetoken={}".format(uin,appid,logid,logid,gtk,qzonetoken)
		sad_see_request = requests.get(url,cookies=self.getCookie(self.username)).text
		jsdate = json.loads(sad_see_request[10:-3])
		try:
			for date in range(len(jsdate['data']['list'])):
				if starttime == None and stoptime == None:
					print("发布说说的QQ号: ",uin,"看了这条说说的QQ号:", jsdate['data']['list'][date]['uin'],'访问时间: ', datetime.fromtimestamp(jsdate['data']['list'][date]['time']),"用户名: ", jsdate['data']['list'][date]['name'])
					self.sql.save(jsdate['data']['list'][date]['uin'], uin, logid)
				elif str(starttime) <= str(datetime.fromtimestamp(jsdate['data']['list'][date]['time']))[0:4] and str(stoptime) >= str(datetime.fromtimestamp(jsdate['data']['list'][date]['time']))[0:4]:
					print("发布说说的QQ号: ",uin,"看了这条说说的QQ号:", jsdate['data']['list'][date]['uin'],'访问时间: ',datetime.fromtimestamp(jsdate['data']['list'][date]['time'],"用户名: ",jsdate['data']['list'][date]['name']))
					self.sql.save(jsdate['data']['list'][date]['uin'], uin, logid)
				else:
					pass    # 方便扩展~
		except KeyError:
			print("抱歉，由于对方设置，您没有权限查看这些访客")

	# 获取个人空间信息（说说、日志、留言、相册）总数
	def get_strip_data(self,sid='',uin=''):
		url = "https://mobile.qzone.qq.com/profile?sid={}&hostuin={}&no_topbar=1&srctype=10&stat=&g_f=2000000209#mine?res_uin={}&ticket=".format(
			sid, uin, uin)
		dc = {}
		strip_request = requests.get(url,headers=self.headers,cookies=self.getCookie(self.username)).text
		Bs = BeautifulSoup(strip_request, 'lxml')
		bfind = Bs.find_all('script', type="application/javascript")[-1]
		get_first_time = re.compile(r'"time":.*?}')
		get_count_and_profile = re.compile(r'{"birthday":{"undealnum":0},.*?}}')
		for attachinfo in bfind:
			dc['time'] = json.dumps(get_first_time.findall(attachinfo)[0][7:-1])
		for count in bfind:
			data = json.loads(get_count_and_profile.findall(count)[0])
			dc['blog'] = data['count']['blog']
			dc['message'] = data['count']['message']
			dc['pic'] = data['count']['pic']
			dc['shuoshuo'] = data['count']['shuoshuo']
			dc['age'] = data['profile']['age']
			dc['nickname'] = data['profile']['nickname']
		return dc

	def get_fristdotai_time(self,sid):
		url = "https://mobile.qzone.qq.com/?sid={}".format(sid)
		strip_request = requests.get(url, headers=self.headers, cookies=self.getCookie(self.username)).text
		Bs = BeautifulSoup(strip_request, 'lxml')
		bfind = Bs.find_all('script', type="application/javascript")[-1]
		loginuin = re.compile(r'loginUin : .*?,')
		attachinfo = re.compile(r'"attachinfo":".*?"')
		appid = re.compile(r'"appid":.*?,')
		times = re.compile(r'"time":.*?,"a')
		datedict = {}
		for date in bfind:
			datedict['loginuin'] = loginuin.findall(date)[0][12:-2]
			datedict['times'] = times.findall(date)[0][7:-3]
			# print(loginuin.findall(date)[0][12:-2])
			# # print(attachinfo.findall(date)[0])
			# # print(appid.findall(date)[])
			# print(times.findall(date)[0][7:-3])
		return datedict

	# 获取好友发送的动态说说~
	def get_dotai_sad(self,loginuin,qzone,gtk,times):
		pagenum = 0
		UnReadSum = 0
		while True:
			url = "https://user.qzone.qq.com/proxy/domain/ic2.qzone.qq.com/cgi-bin/feeds/feeds3_html_more?uin={}&scope=0&view=1&daylist=&uinlist=&gid=&flag=1&filter=all&applist=all&refresh=0&aisortEndTime=0&aisortOffset=0&getAisort=0&aisortBeginTime=0&pagenum={}&externparam=basetime%3D{}%26pagenum%3D{}%26dayvalue%3D0%26getadvlast%3D1%26hasgetadv%3D35883872%5E0%5E1507032145%26lastentertime%3D0%26LastAdvPos%3D1%26UnReadCount%3D{}%26UnReadSum%3D56%26LastIsADV%3D1%26UpdatedFollowUins%3D1927997462%26UpdatedFollowCount%3D1%26LastRecomBrandID%3D&firstGetGroup=0&icServerTime=0&mixnocache=0&scene=0&begintime={}&count=10&dayspac=0&sidomain=qzonestyle.gtimg.cn&useutf8=1&outputhtmlfeed=1&rd=0.9119146146117596&usertime=1507032286939&windowId=0.5806857502490512&g_tk={}&qzonetoken={}".format(
				loginuin, pagenum, times, pagenum, UnReadSum, times, gtk, qzone)
			strip_request = requests.get(url, headers=self.headers, cookies=self.getCookie(self.username)).text
			jsdate = strip_request[10:-3]
			nickname = re.compile(r'nickname:.*?,')    # 发送者的名字
			abstime = re.compile(r'abstime:.*?,')    # 发送时间
			uin = re.compile(r'opuin:.*?,')   # 发送者的QQ号
			key = re.compile(r'typeid:.*?,key:.*?,flag')    # 说说id
			appid = re.compile(r'ver:.*?,appid:.*?,')    # appid
			date_dict = {}
			try:
				times = abstime.findall(jsdate)[-1].split(':')[1][1:-2]    # 得到最后一个说说的发送时间
				for date in range(len(nickname.findall(jsdate))):
					print('发送者: ',nickname.findall(jsdate)[date].split(':')[1][1:-2].split("'")[0],
						  "发送者QQ:",uin.findall(jsdate)[date].split(':')[1][1:-1].split("'")[0],
						  '发送时间: ',datetime.fromtimestamp(int(abstime.findall(jsdate)[date].split(':')[1][1:-2])),
						  '说说id: ',key.findall(jsdate)[date].split(':')[2][1:-6])
					date_dict['nickname'] = nickname.findall(jsdate)[date].split(':')[1][1:-2].split("'")[0]
					date_dict['abstime'] = abstime.findall(jsdate)[date].split(':')[1][1:-2]
					date_dict['uin'] = uin.findall(jsdate)[date].split(':')[1][1:-1].split("'")[0]
					date_dict['key'] = key.findall(jsdate)[date].split(':')[2][1:-6]
					date_dict['appid'] = appid.findall(jsdate)[date].split(':')[-1][1:-2]
					self.get_sad_see(date_dict['uin'],date_dict['appid'],date_dict['key'],self.get_gtk(self.getCookie(self.username)),self.get_qzonetoken(self.getCookie(self.username)))
				pagenum += 1
				pagenum += 10
			except IndexError:
				print("你的QQ号没有好友更新说说~")
				break

	# 获取自己发送的说说
	def get_sad_date(self,qzone,gtk,uin,times,sid):
		doffset = 0
		lastrefreshtime = int(time.time())
		loadcount = 0
		while True:
			attachinfo = "att%3Dback%255Fserver%255Finfo%253Doffset%25253D{}%252526total%25253D10%252526basetime%25253D{}%252526feedsource%25253D0%2526lastrefreshtime%253D{}%2526lastseparatortime%253D0%2526loadcount%253D{}%26tl%3D{}".format(doffset,times,lastrefreshtime,loadcount,times)
			url = "https://mobile.qzone.qq.com/get_feeds?qzonetoken={}&g_tk={}&hostuin={}&res_type=2&res_attach={}&refresh_type=2&format=json&sid={}".format(qzone,gtk,uin,attachinfo,sid)
			true = ""
			false = ""
			null = ''
			data = requests.get(url,cookies=self.getCookie(self.username)).text
			jsdata = json.loads(data)
			times_list = []
			try:
				for dates in zip(range(len(jsdata['data']['vFeeds'])),jsdata['data']['vFeeds']):
					print('Title:',jsdata['data']['vFeeds'][dates[0]]['operation']['share_info']['title'],'Time:',datetime.fromtimestamp(dates[1]['comm']['time']),'id:',dates[1]['id']['cellid'])
					self.get_sad_see(dates[1]['userinfo']['user']['uin'],dates[1]['comm']['appid'],dates[1]['id']['cellid'],self.get_gtk(self.getCookie()),self.get_qzonetoken(self.getCookie()))
					times_list.append(dates[1]['comm']['time'])
					time.sleep(1)
				times = times_list[-1]
				doffset+=10
				loadcount+=1
			except KeyError:
				print("说说已全部获取!")
				break

	def login(self):
		print("开始输入账号和密码....")
		u = self.browser.find_element_by_xpath('//*[@id="u"]')
		p = self.browser.find_element_by_xpath('//*[@id="p"]')
		go = self.browser.find_element_by_xpath('//*[@id="go"]')
		u.clear()    # 清空账号输入框的内容
		action = ActionChains(self.browser)    # 模拟键盘输入
		action.move_to_element(u).click().send_keys(self.username)   # 移动到账号输入框并选中，然后输入账号
		action.move_to_element(p).click().send_keys(self.password)   # 移动到密码输入框并选中，然后输入密码
		action.move_by_offset(go.location['x'],go.location['y'])
		action.click(go)
		action.perform()
		time.sleep(3)
		self.browser.save_screenshot('ceshi1.png')
		if self.browser.title != "QQ空间":
			print("需要验证~")
			time.sleep(2)
			self.fuck_verify_code()
		else:
			print("登陆成功!,正在保存cookie....")
			cookie = {}
			for c in self.browser.get_cookies():
				cookie[c['name']] = c['value']
			self.sava_cookie(self.username,cookie)
			print("正在爬取!")
			self.get_dotai_sad(self.get_fristdotai_time(self.get_sid(self.browser.page_source))['loginuin'],self.get_qzonetoken(self.getCookie(self.username)),self.get_gtk(self.getCookie(self.username)),self.get_fristdotai_time(self.get_sid(self.browser.page_source))['times'])
			print("OVER")

	def __del__(self):
		self.browser.quit()

if __name__ == '__main__':
	name = ""
	pw = ""
	print("获取账号和密码......")
	with open('number.txt','r') as f:
		number = f.readlines()
	name = number[0].strip()
	pw = number[1]
	print("获取成功!")
	qq = qzone_login(username=name,password=pw)
	qq.login()