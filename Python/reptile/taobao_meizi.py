import requests
from bs4 import BeautifulSoup
import os
import json
import re

class TaobaoMeizi:

    def __init__(self):
        self.data = {'q': '',
                    'viewFlag': 'A',
                    'sortType': 'default',
                    'searchStyle': '',
                    'searchRegion': 'city:',
                    'searchFansNum': '',
                    'currentPage': 1,
                    'pageSize': 100}

        self.headers = {"user-agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"}
        self.model_information_list = []
        self.session = requests.session()

    def get_everone_model_information(self):
        url = "https://mm.taobao.com/tstar/search/tstar_model.do?_input_charset=utf-8"
        resp = self.session.post(url, headers=self.headers, data=self.data)
        # print(resp.cookies.get_dict())
        json_resp = json.loads(resp.text)
        print("开始爬取第 {} 页的所有模特信息".format(json_resp['data']['currentPage']))
        for information in json_resp['data']['searchDOList']:
            data_dict = {}
            data_dict['realname'] = information['realName']
            data_dict['userid'] = information['userId']
            height = information['height']
            weight = information['weight']
            city = information['city']
            print("模特: {} 身高: {} 体重: {} 城市: {} id: {}".format(data_dict['realname'], height, weight, city, data_dict['userid']))
            self.model_information_list.append(data_dict)

    def get_model_all_photo(self):
        flag = True
        while flag:
            data = self.model_information_list.pop()
            print("正在获取模特: {} 的所有相册......".format(data['realname']))
            # self.get_all_photo(data['userid'], data['realname'])
            userid = data['userid']
            realname = data['realname']
            if self.model_information_list == []:
                break
            flags = True
            page = 1
            while flags:
                url = "https://mm.taobao.com/self/album/open_album_list.htm?_charset=utf-8&user_id%20={}&page={}".format(userid, page)
                photo_resp = requests.get(url, headers=self.headers).text
                bsoup = BeautifulSoup(photo_resp, 'lxml')
                bfind_title = bsoup.find_all('h4')  # 获取相册的标题
                bfind_first = bsoup.find_all('a', class_="mm-first")
                bfind_pic_number = bsoup.find_all('span', class_="mm-pic-number")
                re_album_id = re.compile(r'album_id=(.*?)&amp;')  # 匹配album id
                re_img_dict = re.compile(r'<input type="hidden" value="\[(.*?)\]')
                re_picid = re.compile(r'&quot;picId&quot;:&quot;(.*?)&quot;')  # 获取每张图片的id
                get_album_id = re_album_id.findall(str(bfind_first))    # 得到album id
                title = [i.get_text().strip() for i in bfind_title]  # 去除标题中的空格
                photo_number = [i.get_text().strip()[1:-2] for i in bfind_pic_number]     # 每个相册的图片总数
                if bfind_title == []:
                    print("模特 {} 爬完了~".format(realname))
                    break
                for album_id, title, photo_num in zip(get_album_id, title, photo_number):
                    photo_url = "https://mm.taobao.com/photo-{}-{}.htm".format(userid, album_id)
                    resp = requests.get(photo_url).text
                    get_img = re_img_dict.search(resp)
                    get_pic = re_picid.findall(get_img.groups()[0])
                    print("正在下载 {} 的相册 {} 共计图片 {}...".format(realname, title, photo_num))
                    for pic_id in get_pic:
                        cookies = self.session.cookies.get_dict()    # 没有cookie就没法得到json
                        # 要想得到json~要提交post
                        data = {
                            'album_user_id': userid,
                            '_tb_token_': cookies['_tb_token_'],
                            'pic_id': pic_id,
                            'album_id': '',
                            'is_edit': 'true'
                        }
                        get_photo_url = "https://mm.taobao.com/album/json/get_photo_data.htm?_input_charset=utf-8"
                        get_photo_resp = self.session.post(get_photo_url, headers=self.headers, data=data, cookies=cookies).text
                        replace_str = (get_photo_resp.replace('false', '"false"')).replace('true', '"true"')
                        try:
                            img_url = (json.loads(replace_str)['photo_url']).replace('_620x10000.jpg', '')[2:]
                            # print(img_url)
                            self.download(realname, title, img_url)
                        except json.JSONDecodeError:
                            replace_strs = (get_photo_resp.replace('false', '"false"')).replace('true', '"true"')
                            re_pic_url = re.compile(r'"picUrl":"//(.*?)",')
                            for img_url in re_pic_url.findall(replace_strs):
                                # print(img_url)
                                self.download(realname, title, img_url)
                    print("相册 {} 爬取完成!".format(title))
                page += 1

    def download(self, modelname, photo, img_url):
        try:
            os.mkdir('TaoBaoModel')
            os.mkdir("TaoBaoModel/{}".format(modelname))
        except FileExistsError:
            pass
        try:
            os.mkdir("TaoBaoModel/{}/{}".format(modelname, photo))
        except FileExistsError:
            pass
        try:
            with open("TaoBaoModel/{}/{}/{}.{}".format(modelname, photo, (img_url.split("/")[4]).split("_")[0], img_url.split('.')[-1]), 'wb') as d:
                resp = requests.get("http://"+img_url, headers=self.headers, cookies=self.session.cookies.get_dict())
                d.write(resp.content)
        except FileNotFoundError:
            pass

    def main(self):
        self.get_everone_model_information()
        self.get_model_all_photo()

if __name__ == '__main__':
    taobaomeizi = TaobaoMeizi()
    taobaomeizi.main()