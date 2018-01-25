import requests
import re
import os
from bs4 import BeautifulSoup
from urllib.request import urlretrieve

class Xiaohua():
    try:
        os.mkdir('xiaohua')
    except FileExistsError:
        pass

    def __init__(self):
        self.url_list = []
        self.headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"}

    def get_page(self):
        url = "http://www.xiaohuar.com/hua/"
        get_request_page = requests.get(url,headers=self.headers).text
        Bsoup = BeautifulSoup(get_request_page, 'lxml')
        Bfind = Bsoup.find('div', class_="page_num").find_all('a')
        re_str = re.compile(r'<a href="http://www.xiaohuar.com/list-1-(\d+).html">尾页</a>')
        page = int(re_str.search(str(Bfind[-1])).groups()[0])+1
        return page

    def get_image_url(self, page):
        print("正在获取第 {} 页的校花相册地址......".format(page+1))
        url = "http://www.xiaohuar.com/list-1-{}.html".format(page)
        request_url = requests.get(url, headers=self.headers).text
        img_url_soup = BeautifulSoup(request_url, 'lxml')
        img_find = img_url_soup.find('div', class_="demo clearfix").find_all('div', class_="img")
        re_name = re.compile(r'<a href="(.*?)" target="_blank"><img alt="(.*?)" src')
        for img in img_find:
            link = re_name.search(str(img)).groups()
            self.url_list.append(re_name.search(str(img)).groups()[0].replace('p-','s-'))
            print("正在获取 '{}' 的相册地址".format(link[1]))
        print("第 {} 页的校花相册地址获取完成!".format(page))
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        return self.url_list.sort(reverse=False)

    def download(self,image_site,name):
        print("正在下载 `{}`.....".format(image_site.split('/')[-1]))
        url = "http://www.xiaohuar.com"+image_site
        try:
            os.mkdir('xiaohua/{}'.format(name))
        except FileExistsError:
            pass
        urlretrieve(url, 'xiaohua/{}/{}.{}'.format(name, image_site.split('/')[-1][0:-4], image_site.split('.')[-1]))

    def get_xiaohua_total_img(self):
        for i in range(len(self.url_list)):
            url = self.url_list.pop()
            img_request = requests.get(url, headers=self.headers).text
            bs = BeautifulSoup(img_request, 'lxml')
            bfind_name = bs.find('div', class_="pic_con_box ad-gallery").find_all('h1')
            re_name = re.compile(r'<h1>(.*?)<span class')
            xiaohau_name = re_name.search(str(bfind_name[0])).groups()[0]
            bfind = bs.find('ul', class_="ad-thumb-list").find_all('a')
            re_img = re.compile(r'<a class="" href="(.*?)"')
            print("开始下载 `{}`".format(xiaohau_name))
            for img in bfind:
                imgs = re_img.search(str(img)).groups()[0]
                self.download(imgs,xiaohau_name)
            print("校花 `{}` 下载完成~".format(xiaohau_name))
            print("***************************************")
            if self.url_list == []:
                break

    def main(self):
        page = self.get_page()
        for num in range(page):
            self.get_image_url(num)
            self.get_xiaohua_total_img()
        print("爬取完成!")

if __name__ == '__main__':
    x = Xiaohua()
    x.main()