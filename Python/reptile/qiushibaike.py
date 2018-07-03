# -*- coding: utf-8 -*-
# @Time    : 2018/5/5 19:08
# @Author  : Ape Code
# @FileName: qiushibaike.py
# @Software: PyCharm
# @Blog    ：https://www.liuyangxiong.cn

import requests
from bs4 import BeautifulSoup


class QiuShiBaiKe:

    # 初始化
    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) "
                                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                                      "Chrome/66.0.3359.139 Safari/537.36"}
        self.spiderContent = {'首页': '8hr',
                              '24小时': 'hot',
                              '热图': 'imgrank',
                              '文字': 'text',
                              '穿越': 'history',
                              '糗图': 'pic',
                              '新鲜':'textnew'}    # 网站的目录
        self.url = "https://www.qiushibaike.com/" + self.spiderContent['首页']     # 爬取的内容在此切换
        self.articleList = []    # 内容的url地址

    # 得到页数
    def getPageNum(self):
        response = requests.get(self.url, headers=self.headers).text
        bsoup = BeautifulSoup(response, 'lxml')
        bfind_pagenum = bsoup.find('ul', class_='pagination').find_all('span', class_='page-numbers')[-1].get_text().strip()    # 得到总页数
        return bfind_pagenum

    # 返回每页页面内容的url
    def returnUrl(self, page):
        homeUrlResponse = requests.get(self.url + "/page/{}/".format(str(page)), headers=self.headers).text
        homebsoup = BeautifulSoup(homeUrlResponse, 'lxml')
        homebfind = homebsoup.find('div', class_="col1").find_all('a', class_="contentHerf")    # 获取每页内容的所有url链接
        for all_href in homebfind:
            self.articleList.append(all_href['href'])
        return self.articleList

    # 获取用户发送的文字内容或者是文字+图片的内容，用来爬取混合的目录~就是文字内容和文字+图片内容都有的那种~例如爬取首页
    def getMixingContent(self, url):    # 参数: returnUrl返回的url地址
        responseContent = requests.get(url="https://www.qiushibaike.com" + url, headers=self.headers).text
        bsoupContent = BeautifulSoup(responseContent, 'lxml')
        bfindIsPic = bsoupContent.find('div', class_='thumb')   # 用来查看用户发送的内容是否带有图片
        bfindContent = bsoupContent.find('div', class_='content').get_text()    # 获取文字内容
        if bfindIsPic == None:    # 如果返回值为None，则判断为文字内容
            print(bfindContent.strip())
        else:
            bfindPic = bsoupContent.find('div', class_='thumb').find_all('img')    # 获取图片
            pic_alt = bfindPic[0]['alt']    # 图片的标题
            pic_link = bfindPic[0]['src']    # 图片的链接
            print(bfindContent.strip())
            print(pic_alt + pic_link[2:])

    # 爬取文字内容
    def getContent(self, url):
        pass

    # 爬取文字+图片内容
    def getContentAndPic(self, url):
        pass

    # 获取评论
    def getComment(self, url):
        pass

    # Run
    def main(self):
        page = int(self.getPageNum())
        num = 1
        while page >= num:
            self.returnUrl(num)
            print("--------------------------------")
            print(self.articleList)
            while True:
                self.articleList.reverse()
                contentURl = self.articleList.pop()
                # self.getContent(contentURl)
                self.getMixingContent(contentURl)
                if self.articleList == []:
                    print("ok")
                    break
            num += 1

if __name__ == '__main__':
    QSBK = QiuShiBaiKe()
    QSBK.main()
