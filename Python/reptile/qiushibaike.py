# -*- coding: utf-8 -*-
# @Time    : 2018/5/5 19:08
# @Author  : Ape Code
# @FileName: qiushibaike.py
# @Software: PyCharm
# @Blog    ：https://www.liuyangxiong.cn

import requests
from bs4 import BeautifulSoup


class Qiushibaike:

    # 初始化
    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) "
                                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                                      "Chrome/66.0.3359.139 Safari/537.36"}
        self.url = "https://www.qiushibaike.com"
        self.articleList = []    # 内容的url地址

    # 返回每条内容的url
    def returnUrl(self, content):   # 参数: / hot imgrank text history pic textnew
        homeUrlResponse = requests.get(self.url + content, headers=self.headers).text
        homebsoup = BeautifulSoup(homeUrlResponse, 'lxml')
        homebfind = homebsoup.find('div', class_="col1").find_all('a', class_="contentHerf")    # 获取每页内容的所有url链接
        for all_href in homebfind:
            self.articleList.append(all_href['href'])
        return self.articleList

    # 获取用户发送的内容
    def getContent(self, url):    # 参数: returnUrl返回的
        pass

    # Run
    def main(self):
        # 默认爬取首页的,其他内容 hot imgrank text history pic textnew
        spiderContent = "/8hr/page/{}/".format(1)
        print(self.returnUrl(spiderContent))
        pass


if __name__ == '__main__':
    qiushibaike = Qiushibaike()
    qiushibaike.main()