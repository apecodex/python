import json
import os,sys
import pickle
import requests
from urllib import request
import time
import threading
from multiprocessing import Process
from mysqlite import MySqlite
from Friend_qq_number import QQ_number

class Sqlite(MySqlite):

    def __init__(self):
        MySqlite.__init__(self)

class Myqq(QQ_number):

    def __init__(self):
        QQ_number.__init__(self)

class Shuoshuo_key():

    def __init__(self):
        self.headers = {"user-agent": "Mozilla/5.0 (Linux; U; Android 2.3.6; zh-cn; GT-S5660 Build/GINGERBREAD) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1 MicroMessenger/4.5.255"}

    def read_token(self):
        with open('token_gtk_sid.txt', 'r') as rt:
            return json.load(rt)['qzonetoken']

    def read_gtk(self):
        with open('token_gtk_sid.txt') as rt:
            return json.load(rt)['gtk']

    def read_sid(self):
        with open('token_gtk_sid.txt', 'r') as rt:
            return json.load(rt)['sid']

    def getCookie(self):
        with open("token_gtk_sid.txt",'r') as rc:
            return json.loads(json.load(rc)['cookie'])

        # try:
        #     with open("cookie.txt", 'rb') as f:
        #         cookie = pickle.load(f)
        #     return cookie
        # except EOFError:
        #     pass

    def get_firend_shuoshuo(self, firend_qq):
        # sqlite = Sqlite()
        print("开始爬取QQ '{}'...".format(firend_qq))
        proxies = {
            'http': 'http://110.73.51.151',
            'https': 'https://123.156.178.82'
        }
        url = "https://mobile.qzone.qq.com/list?qzonetoken={}&g_tk={}&format=json&list_type=shuoshuo&action=0&res_uin={}&count=10".format(
            self.read_token(), self.read_gtk(), firend_qq)
        request_shuoshuo_first_url = requests.get(url, headers=self.headers, cookies=self.getCookie())
        json_data = json.loads(request_shuoshuo_first_url.text)
        message = "操作过于频繁咯！休息会再来操作吧！"
        if json_data['message'] == "请先登录":
            print("被冻结了.....换号吧~")
            os._exit(1)
        elif json_data['message'] == message:
            print("操作过于频繁咯！缓60秒")
            with open("token_gtk_sid.txt", 'r') as f:
                data = json.load(f)
                qq = data['qq']
                Sqlite().del_cookie(qq)
            # time.sleep(60)
            main()
            # os._exit(0)
            # sys.exit(0)
        else:
            try:
                Sqlite().del_undone_qq_number_and_del_beijing_qq_number_and_sava_completed_qq_number(firend_qq)
                for num in range(len(json_data['data']['vFeeds'])):
                    # print("保存QQ '{}' 的说说".format(firend_qq))
                    print("保存QQ '{}' 的说说".format(firend_qq), json_data['data']['vFeeds'][num]['comm']['feedskey'])
                    Sqlite().sava_undone_shuoshuo_key(firend_qq,json_data['data']['vFeeds'][num]['comm']['appid'],json_data['data']['vFeeds'][num]['comm']['feedskey'])
                    Sqlite().sava_undone_summary_key(firend_qq,json_data['data']['vFeeds'][num]['comm']['feedskey'])
                # self.get_sad_see(firend_qq,json_data['data']['vFeeds'][num]['comm']['appid'],json_data['data']['vFeeds'][num]['comm']['feedskey'],self.read_gtk(),self.read_token())
                # time.sleep(1)
                att = request.quote(json_data['data']['attach_info'])
                num = 100  # 最多爬多少说说
                while num >= 0:
                    urls = "https://mobile.qzone.qq.com/list?qzonetoken={}&g_tk={}&res_attach={}&format=json&list_type=shuoshuo&action=0&res_uin={}&count=10".format(
                        self.read_token(), self.read_gtk(), att, firend_qq)
                    while_request_shuoshuo_url = requests.get(urls, headers=self.headers,cookies=self.getCookie())
                    json_data = json.loads(while_request_shuoshuo_url.text)
                    try:
                        for num in range(len(json_data['data']['vFeeds'])):
                            # print("保存QQ '{}' 的说说".format(firend_qq))
                            print("保存QQ '{}' 的说说".format(firend_qq),json_data['data']['vFeeds'][num]['comm']['feedskey'])
                            Sqlite().sava_undone_shuoshuo_key(firend_qq,json_data['data']['vFeeds'][num]['comm']['appid'],json_data['data']['vFeeds'][num]['comm']['feedskey'])
                            Sqlite().sava_undone_summary_key(firend_qq,json_data['data']['vFeeds'][num]['comm']['feedskey'])
                            num -= 1
                    except KeyError:
                        print(firend_qq, "爬取完成!")
                        break
                    finally:
                        att = request.quote(json_data['data']['attach_info'])
            except KeyError:
                pass

def change_cookie():
    print("--------------------------------")
    print("开始切换cookie...................|")
    print("--------------------------------")
    time.sleep(5)
    cookies = Sqlite().read_cookie()
    cookie_and_args = {}
    cookie_and_args['qq'] = cookies[0]
    cookie_and_args['cookie'] = cookies[1]
    cookie_and_args['gtk'] = cookies[2]
    cookie_and_args['sid'] = cookies[3]
    cookie_and_args['qzonetoken'] = cookies[4]

    with open("token_gtk_sid.txt", 'w') as tgs:
        json.dump(cookie_and_args,tgs)


def get_firend_qq(file="QQForSpider.txt"):
    number = []
    with open(file,'r') as f:
        number = f.read().split("\n")
    if number == [""]:
        print("QQForSpider文件中没有初始化QQ")
    else:
        return number

def main():
    sqlite = Sqlite()
    my = QQ_number()
    shuo = Shuoshuo_key()
    QQForSpider_number = get_firend_qq()
    for num in QQForSpider_number:
        if my.firend_permission(num) == 1:
            sqlite.sava_undone_qq_number_and_sava_information_qq_number(num)
            print("{} 可以正常访问~".format(num))
        else:
            print("{} 没有权限访问......".format(num))
            sqlite.del_undone_qq_number_and_del_beijing_qq_number_and_sava_completed_qq_number(num)
    numbers = Sqlite().read_5_duilie()
    if numbers == []:
        print("请运行Firend_qq_number 获取一些QQ号吧~")
    else:
        while numbers:
            if numbers == []:
                print("请运行Firend_qq_number 获取一些QQ号吧~")
            numbers = Sqlite().read_5_duilie()
            print("从数据库中获取QQ号: '{}'".format(numbers))
            for num in numbers:
                # shuo.get_firend_shuoshuo(num)
                p = Process(target=shuo.get_firend_shuoshuo,args=(num,))
                p.start()
                # t = threading.Thread(target=shuo.get_firend_shuoshuo,args=(num,))
                # t.setDaemon(True)
                # t.start()
            # t.join()
            p.join()
            change_cookie()

if __name__ == '__main__':
    main()
