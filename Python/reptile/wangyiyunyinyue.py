import requests
import json
from bs4 import BeautifulSoup
import numpy as np
import time
import sqlite3
import os
import base64

class Wangyiyunyinyue():

	def __init__(self,url):
		self.connent_sql = sqlite3.connect("wangyiyunyinyue.db")
		self.cursor = self.connent_sql.cursor()
		self.headers = {
			"Accept":"*/*",
			"Connection":"keep-alive",
			"User-Agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36"
		}
		self.proxies = {'https':'https://61.183.176.122','https':'https://121.32.122.37'}
		self.url = url

	def sql(self,song_id,singer,song_name,alium,lyric):
		sql = """
		CREATE table IF NOT EXISTS song_information(
			song_id VARCHAR NOT NULL,
			singer VARCHAR NOT NULL,
			song_name VARCHAR NOT NULL,
			alium VARCHAR NOT NULL,
			lyric VARCHAR NOT NULL
		);
		"""
		self.cursor.execute(sql)
		self.connent_sql.commit()

		data = "INSERT INTO song_information (song_id,singer,song_name,alium,lyric) VALUES ('{}','{}','{}','{}','{}')".format(song_id,singer,song_name,alium,lyric)
		self.cursor.execute(data)
		self.cursor.close()
		self.connent_sql.commit()
		self.connent_sql.close()

	def check_sql(self):
		date = "SELECT * FROM song_information"
		a = self.cursor.execute(date)
		for i in a:
			print(i)

	def


w = Wangyiyunyinyue("as")
# w.sql("1","2","3","4","5")
# w.check_sql()
# def sql():
# 	connent_sql = sqlite3.connect("wangyiyunyinyue.db")
# 	cursor = connent_sql.cursor()
# 	sql = """
# 	CREATE table song_information(
# 		singer VARCHAR NOT NULL,
# 		song_name VARCHAR NOT NULL,
# 		alium VARCHAR NOT NULL
# 	);
# 	"""
# 	# if os.path.exists("wangyiyunyinyue.db") == False:
# 	cursor.execute(sql)
# 	cursor.close()
# 	connent_sql.commit()
# 	connent_sql.close()
#
# def sava_sql(song,singer,alium):
# 	if os.path.exists("wangyiyunyinyue.db"):
# 		pass
# 	else:
# 		sql()
# 	connent_sql = sqlite3.connect("wangyiyunyinyue.db")
# 	cursor = connent_sql.cursor()
# 	date = "INSERT INTO song_information (singer,song_name,alium) VALUES ('{}','{}','{}');".format(song, singer, alium)
# 	date2 = "SELECT * FROM song_information;"
# 	x = cursor.execute(date)
# 	# a = 1
# 	# for i in x:
# 	# 	print(a,"歌曲:",base64.b64decode(str.encode(i[0])).decode("utf-8"),"\t",
# 	# 		  "歌手:",base64.b64decode(str.encode(i[1])).decode("utf-8"),"\t",
# 	# 		  "专辑:",base64.b64decode(str.encode(i[2])).decode("utf-8"))
# 	# 	a+=1
# 	cursor.close()
# 	connent_sql.commit()
# 	connent_sql.close()
#
#
# headers = {
# 	"Accept":"*/*",
# 	"Connection":"keep-alive",
# 	"User-Agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36"
# }
# proxies = {'https':'https://61.183.176.122','https':'https://121.32.122.37'}
# url = "http://music.163.com/api/v3/playlist/detail?id=777996085"
# r = requests.get(url,headers=headers,timeout=10,proxies=proxies)
# js = json.loads(r.text)
# a = 1
# for ids in js['playlist']['trackIds']:
# 	song_url = "http://music.163.com/song?id={}".format(ids['id'])
# 	lyric_url = "http://music.163.com/api/song/lyric?id={}&lv=-1&kv=-1&tv=-1".format(ids['id'])
# 	res = requests.get(song_url,headers=headers,timeout=10,proxies=proxies)
# 	res_text = res.text
# 	BS = BeautifulSoup(res_text,'lxml')
# 	song_name = BS.find("div",class_="cnt").find_all("div",class_="tit")
# 	singer_and_album = BS.find("div",class_="cnt").find_all("p")
# 	song_information = []
# 	for sn in song_name:
# 		song_information.append(base64.b64encode(str.encode(sn.get_text().strip())))
# 		for saa in singer_and_album:
# 			song_information.append(base64.b64encode(str.encode(saa.get_text().split("：")[1])))
# 	res_lyric = requests.get(lyric_url,headers=headers,proxies=proxies)
# 	js = res_lyric.json()
# 	time.sleep(np.random.random())
# 	try:
# 		English_lyric = js['lrc']['lyric']
# 		chinese_lyric = js['tlyric']['lyric']
# 		print("歌曲:"+base64.b64decode(song_information[0]).decode("utf-8"),
# 			  "歌手:"+base64.b64decode(song_information[1]).decode("utf-8"),
# 			  "专辑:"+base64.b64decode(song_information[2]).decode("utf-8"),
# 			  "歌词:",js['lrc'])
# 		try:
# 			with open("ceshi/{}.lrc".format(ids['id']),'a') as f:
# 				f.write(English_lyric)
# 				f.write(chinese_lyric)
# 		except TypeError:  # 有些要么只有英文的，要么只有中文的，要么就没有歌词
# 			pass
# 		# sava_sql(song_information[0].decode("utf-8"),song_information[1].decode("utf-8"),song_information[2].decode("utf-8"))
# 	except KeyError:
# 		pass
# 	except UnicodeEncodeError:
# 		print("GBK!")
# 	a+=1
