import requests
from bs4 import BeautifulSoup
import numpy as np
import time
import sqlite3
import os
import base64
import pymysql

class Wangyiyunyinyue():

	def __init__(self,user,password,db,url):
		self.connent_sql = pymysql.connect(user='{}'.format(user),
					  password="{}".format(password),
					  host="127.0.0.1",
					  port=3306,
					  db="{}".format(db))
		self.cursor = self.connent_sql.cursor()
		self.headers = {
			"Accept":"*/*",
			"Connection":"keep-alive",
			"User-Agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36"
		}
		self.proxies = {'https':'https://61.183.176.122','https':'https://121.32.122.37'}
		self.url = url

	def sql(self):
		sql = """
		CREATE TABLE IF NOT EXISTS song_information(
			playlist_id VARCHAR(20),
			song_id VARCHAR(20),
			singer VARCHAR(200),
			song_name VARCHAR(200),
			alium VARCHAR(200),
			lyric VARCHAR(30)
		);

		CREATE TABLE IF NOT EXISTS comment_text(
			song_id VARCHAR(20),
			userId VARCHAR(20),
			nickname VARCHAR(100),
			comment TEXT
		);
		"""
		data = "show tables;"
		self.cursor.execute(data)
		check = self.cursor.fetchall()
		if check == ():
			print("正在创建数据表.....")
			print("数据表创建成功！！！")
			print("---------------------------")
			self.cursor.execute(sql)
			self.connent_sql.commit()
		else:
			pass

	def song_sql(self,playlist_id,song_id,singer,song_name,alium,lyric):
		data = "INSERT INTO song_information (playlist_id,song_id,singer,song_name,alium,lyric) VALUES ('{}','{}','{}','{}','{}','{}')".format(playlist_id,song_id,singer,song_name,alium,lyric)
		self.cursor.execute(data)
		self.connent_sql.commit()


	def comment_sql(self,song_id,userid,nickname,comment):
		data = "INSERT INTO comment_text (song_id,userId,nickname,comment) VALUES ('{}','{}','{}','{}')".format(song_id,userid,nickname,comment)
		self.cursor.execute(data)
		self.connent_sql.commit()

	def check_sql(self):

		date = "SELECT comment_text.comment FROM song_information,comment_text WHERE song_information.song_id=comment_text.song_id and song_information.song_id=3423803"
		# date = "SELECT * FROM song_information;"
		self.cursor.execute(date)
		results = self.cursor.fetchall()
		# print(a)
		x = 1
		for i in results:
			# print(x,i[0],base64.b64decode(str.encode(i[1])).decode("utf-8"),base64.b64decode(str.encode(i[-1])).decode("utf-8"))
			# print(x,"userid:",base64.b64decode(str.encode(i[2])).decode("utf-8"),"内容:",base64.b64decode(str.encode(i[-1])).decode("utf-8"))
			# print(x,base64.b64decode(str.encode(i[2])).decode("utf-8"))
			print(x,base64.b64decode(str.encode(i[0])).decode("utf-8"))
			x+=1

	def song(self,id):
		song_url = "http://music.163.com/song?id={}".format(id)
		ressong = requests.get(song_url,headers=self.headers,proxies=self.proxies,timeout=10)
		Bs = BeautifulSoup(ressong.text,'lxml')
		song_name = Bs.find("div",class_="cnt").find_all("div",class_="tit")
		singer_and_alium = Bs.find("div",class_="cnt").find_all('p')
		song_information = []
		for sn in song_name:
			song_information.append(base64.b64encode(str.encode(sn.get_text().strip())))
			for sa in singer_and_alium:
				song_information.append(base64.b64encode(str.encode(sa.get_text().split("：")[1])))
		try:
			print("歌曲:",base64.b64decode(song_information[0]).decode("utf-8"),
				  "歌手:",base64.b64decode(song_information[1]).decode("utf-8"),
				  "专辑:",base64.b64decode(song_information[2]).decode("utf-8"))
			self.song_sql(self.url.split("=")[-1],id,song_information[1].decode("utf-8"),song_information[0].decode("utf-8"),song_information[2].decode("utf-8"),"lyric/{}/{}.lrc".format(self.url.split("=")[-1],id))
		except KeyError:
			pass
		except UnicodeEncodeError:
			print("GBK")    # windows下 GBK错误~

	def lyric(self,id):
		lyric_url = "http://music.163.com/api/song/lyric?id={}&lv=-1&kv=-1&tv=-1".format(id)
		reslyric = requests.get(lyric_url,headers=self.headers,proxies=self.proxies,timeout=10)
		sp_url = self.url.split("=")[-1]
		try:
			English_lyric = reslyric.json()['lrc']['lyric']
			Chinese_lyric = reslyric.json()['tlyric']['lyric']
			with open("lyric/{}/{}.lrc".format(sp_url,id),'a') as w:
				w.write(English_lyric)
				w.write(Chinese_lyric)
		except KeyError:   #没有歌词的会报错!
			pass
		except TypeError:
			pass    # 有些歌词，要么只有英文,要么只有中文，要么连歌词都没有~~~:)
		except UnicodeEncodeError:    # windows下 GBK错误~
			pass

	def comment(self,id):
		comment_url = "http://music.163.com/api/v1/resource/comments/R_SO_4_{}".format(id)
		rescomment = requests.get(comment_url,headers=self.headers,proxies=self.proxies,timeout=10)
		for cm in range(len(rescomment.json()['hotComments'])):
			userid = rescomment.json()['hotComments'][cm]['user']['userId']
			nickname = rescomment.json()['hotComments'][cm]['user']['nickname']
			comment = rescomment.json()['hotComments'][cm]['content']
			self.comment_sql(id,userid,base64.b64encode(str.encode(nickname)).decode("utf-8"),base64.b64encode(str.encode(comment)).decode("utf-8"))

	def main(self):
		playlist_url = "http://music.163.com/api/v3/playlist/detail?id={}".format(self.url.split("=")[-1])
		reslist = requests.get(playlist_url,headers=self.headers,proxies=self.proxies,timeout=10)
		if reslist.json()['code'] == 404:
			print("URL 地址不对嘛~ -_-!!")
		else:
			self.sql()
			print("正在检测歌单id '{}' 是否在数据库中......".format(self.url.split("=")[-1]))
			data = "SELECT playlist_id FROM song_information WHERE playlist_id={} LIMIT 1;".format(self.url.split("=")[-1])
			self.cursor.execute(data)
			se = self.cursor.fetchall()
			if se != ():
				print("---------------------------")
				print("这个歌单已经在数据库了~请重新换一个歌单~~")
			else:
				if os.path.exists("lyric") == False:
					os.mkdir("lyric")
				if os.path.exists("lyric/{}".format(self.url.split("=")[-1])) == False:
					os.mkdir("lyric/{}".format(self.url.split("=")[-1]))
				print("开始抓取~~~~")
				for ids in reslist.json()['playlist']['trackIds']:
					time.sleep(np.random.random())
					self.song(ids['id'])
					self.lyric(ids['id'])
					self.comment(ids['id'])

if __name__ == "__main__":
	url=""  # 填入歌单的url地址~比如:http://music.163.com/#/playlist?id=864401021
	user=""    # MySQL账号 root
	password=""    # MySQL密码
	db=""    # 数据库名称
	if url == "":
		print("你url地址还没输呐~~")
	else:
		try:
			w = Wangyiyunyinyue(user,password,db,url)
			w.main()
		except pymysql.err.OperationalError:
			print("连接失败~请检查数据库(MySQL)账号或密码是否正确~~~")
