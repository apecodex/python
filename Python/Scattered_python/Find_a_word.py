# -*- coding: utf-8 -*-

"""
统计英文单词出现的个数
"""

import re

def add_word(word, word_dict):
    if word in word_dict:
        word_dict[word]+=1
    else:
        word_dict[word]=1


def Find_word(path="English.txt"):
    time = 1
    with open(path,'r') as f:
        read_word = f.read()
        match = re.findall(r"[^a-zA-Z0-9]+",read_word)
        for i in match:
            read_word = read_word.replace(i," ")
            lines = read_word.split()
        word_dict = {}
        for x in lines:
            add_word(x,word_dict)

        for keys,values in sorted(word_dict.items()):
            time+=1
            print("%3d %-20s %s" % (time,keys,values))





#Find_word()


class FindWord:

	def __init__(self,path="English.txt",word_dict={}):
		self.path = path
		self.word_dict = word_dict

	def find(self):
		print("View all or one(total\one)")
		poi = input("View: ")
		time = 1
		with open(self.path,'r') as f:
			read_word = f.read()
			match = re.findall(r"[^a-zA-Z0-9']+",read_word)
			for i in match:
				read_word = read_word.replace(i," ")
				lines = read_word.split()
			for x in lines:
				if x in self.word_dict:
					self.word_dict[x]+=1
				else:
					self.word_dict[x]=1
			if poi == "total":
				for keys,values in sorted(self.word_dict.items()):
					time+=1
					print("%3d %-20s 出现了‘%s'次" % (time,keys,values))
			elif poi == "one":
				user_input = input("Word: ")
				get_word = self.word_dict.get(user_input,"No Found.")
				print("'%s' 出现了'%s'次" % (user_input,get_word))
			else:
				print("No '%s' parameter" % poi)

s = FindWord()
s.find()
