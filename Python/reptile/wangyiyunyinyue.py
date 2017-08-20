import requests
from bs4 import BeautifulSoup
import numpy as np
import time
import sqlite3
import os
import base64

class Wangyiyunyinyue():

	def __init__(self,url):
		self.headers = {
			"Accept":"*/*",
			"Connection":"keep-alive",
			"User-Agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36"
		}
		self.proxies = {'https':'https://61.183.176.122','https':'https://121.32.122.37'}
		self.url = url

	def sql(self):
		self.connent_sql = sqlite3.connect("wangyiyunyinyue.db")
		self.cursor = self.connent_sql.cursor()
		sql = """
		CREATE table IF NOT EXISTS song_information(
			song_id VARCHAR NOT NULL,
			singer VARCHAR NOT NULL,
			song_name VARCHAR NOT NULL,
			alium VARCHAR NOT NULL,
			lyric VARCHAR NOT NULL
		);
		
		CREATE TABLE IF NOT EXISTS comment_text(
			song_id VARCHAR,
			userId VARCHAR NOT NULL,
			nickname VARCHAR NOT NULL,
			comment TEXT NOT NULL,
			FOREIGN KEY (song_id) REFERENCES song_information (song_id)
		);
		"""
		self.cursor.executescript(sql)
		self.cursor.close()
		self.connent_sql.commit()
		self.connent_sql.close()

	def song_sql(self,song_id,singer,song_name,alium,lyric):
		self.sql()
		self.connent_sql = sqlite3.connect("wangyiyunyinyue.db")
		self.cursor = self.connent_sql.cursor()
		data = "INSERT INTO song_information (song_id,singer,song_name,alium,lyric) VALUES ('{}','{}','{}','{}','{}')".format(song_id,singer,song_name,alium,lyric)
		self.cursor.execute(data)
		self.cursor.close()
		self.connent_sql.commit()
		self.connent_sql.close()

	def comment_sql(self,song_id,userid,nickname,comment):
		self.sql()
		self.connent_sql = sqlite3.connect("wangyiyunyinyue.db")
		self.cursor = self.connent_sql.cursor()
		data = "INSERT INTO comment_text (song_id,userId,nickname,comment) VALUES ('{}','{}','{}','{}')".format(song_id,userid,nickname,comment)
		self.cursor.execute(data)
		self.cursor.close()
		self.connent_sql.commit()
		self.connent_sql.close()

	def check_sql(self):
		self.connent_sql = sqlite3.connect("wangyiyunyinyue.db")
		self.cursor = self.connent_sql.cursor()
		# date = "SELECT comment FROM song_information,comment_text WHERE song_information.song_id==comment_text.song_id"
		date = "SELECT * FROM song_information"
		a = self.cursor.execute(date)
		x = 1
		for i in a:
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
			self.song_sql(id,song_information[1].decode("utf-8"),song_information[0].decode("utf-8"),song_information[2].decode("utf-8"),"lyric/{}/{}.lrc".format(self.url.split("=")[-1],id))
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
		if os.path.exists("lyric") == False:
			os.mkdir("lyric")
		if os.path.exists("lyric/{}".format(self.url.split("=")[-1])) == False:
			os.mkdir("lyric/{}".format(self.url.split("=")[-1]))
		try:
			for ids in reslist.json()['playlist']['trackIds']:
				time.sleep(np.random.random())
				self.song(ids['id'])
				self.lyric(ids['id'])
				self.comment(ids['id'])
		except KeyError:
			print("url地址不对~根本就没这个歌单嘛~~\t-_-!!")

if __name__ == "__main__":
	url = ""  # 填入歌单的url地址~比如:http://music.163.com/#/playlist?id=864401021
	if url == "":
		print("你url地址还没输呐~~")
	else:
		w = Wangyiyunyinyue(url)
		w.main()
