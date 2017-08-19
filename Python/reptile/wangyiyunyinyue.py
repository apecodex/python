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
		"""
		self.cursor.execute(sql)
		self.cursor.close()
		self.connent_sql.commit()
		self.connent_sql.close()
	def sava_sql(self,song_id,singer,song_name,alium,lyric):
		self.connent_sql = sqlite3.connect("wangyiyunyinyue.db")
		self.cursor = self.connent_sql.cursor()
		data = "INSERT INTO song_information (song_id,singer,song_name,alium,lyric) VALUES ('{}','{}','{}','{}','{}')".format(song_id,singer,song_name,alium,lyric)
		self.cursor.execute(data)
		self.cursor.close()
		self.connent_sql.commit()
		self.connent_sql.close()

	def check_sql(self):
		self.connent_sql = sqlite3.connect("wangyiyunyinyue.db")
		self.cursor = self.connent_sql.cursor()
		date = "SELECT * FROM song_information"
		a = self.cursor.execute(date)
		for i in a:
			print(i)

	def main(self):
		playlist_url = "http://music.163.com/api/v3/playlist/detail?id={}".format(self.url.split("=")[-1])
		reslist = requests.get(playlist_url,headers=self.headers,proxies=self.proxies,timeout=10)
		try:
			for ids in reslist.json()['playlist']['trackIds']:
				song_url = "http://music.163.com/song?id={}".format(ids['id'])
				lyric_url = "http://music.163.com/api/song/lyric?id={}&lv=-1&kv=-1&tv=-1".format(ids['id'])
				ressong = requests.get(song_url,headers=self.headers,proxies=self.proxies,timeout=10)
				Bs = BeautifulSoup(ressong.text,'lxml')
				song_name = Bs.find("div",class_='cnt').find_all("div",class_='tit')
				singer_and_alium = Bs.find("div",class_='cnt').find_all('p')
				song_information = []
				for sn in song_name:    #这里因为存不进去~所以改一下编码~
					song_information.append(base64.b64encode(str.encode(sn.get_text().strip())))
					for sa in singer_and_alium:
						song_information.append(base64.b64encode(str.encode(sa.get_text().split("：")[1])))
				time.sleep(np.random.random())
				reslyric = requests.get(lyric_url,headers=self.headers,proxies=self.proxies,timeout=10)
				try:
					English_lyric = reslyric.json()['lrc']['lyric']
					Chinese_lyric = reslyric.json()['tlyric']['lyric']
					print("歌名:",base64.b64decode(song_information[0]).decode("utf-8"),
						  "歌手:",base64.b64decode(song_information[1]).decode("utf-8"),
						  "专辑:",base64.b64decode(song_information[2]).decode("utf-8"))
					self.sava_sql(ids['id'],song_information[1].decode("utf-8"),song_information[0].decode("utf-8"),song_information[2].decode("utf-8"),"chesi/{}.lrc".format(ids['id']))
					try:
						with open("lyric/{}.lrc".format(ids['id']),'a') as w:
							w.write(English_lyric)
							w.write(Chinese_lyric)
					except TypeError:    # 有些歌词，要么只有英文,要么只有中文，要么连歌词都没有~~~:)
						pass
				except KeyError:
					pass
				except UnicodeEncodeError:
					pass  # windows下 GBK错误~
		except KeyError:
			print("url地址不对~根本就没这个歌单嘛~~\t-_-!!")

if __name__ == "__main__":
	url = "http://music.163.com/#/playlist?id=864401021"  #填入歌单的url地址~比如:http://music.163.com/#/playlist?id=864401021
	if os.path.exists("lyric") == False:
		os.mkdir("lyric")
	if url == "":
		print("你url地址还没输呐~~")
	else:
		w = Wangyiyunyinyue(url)
		w.main()
