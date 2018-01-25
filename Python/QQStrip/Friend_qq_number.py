import requests
import json
import pickle
import os
import threading
from multiprocessing import Process,Pool
from mysqlite import MySqlite
from datetime import datetime
import time


class Sqlite(MySqlite):

    def __init__(self):
        MySqlite.__init__(self)

class QQ_number():

    def __init__(self):
        self.headers = {"user-agent": "Mozilla/5.0 (Linux; U; Android 2.3.6; zh-cn; GT-S5660 Build/GINGERBREAD) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1 MicroMessenger/4.5.255"}


    def read_token(self):
        with open('token_gtk_sid.txt', 'r') as rt:
            return json.load(rt)['qzonetoken']

    def read_gtk(self):
        with open('token_gtk_sid.txt','r') as rt:
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

    def get_login_qq_number(self):
        with open('myQQ.txt', 'r') as f:
            number = f.read().strip()
        name = number.split('\n')[0].split(" ")[0]
        return name

    def filter_data(self,friend_qq):
        username = self.get_login_qq_number()
        url = "https://h5.qzone.qq.com/webapp/json/friendSetting/getMainPage?qzonetoken={}&g_tk={}&uin={}&visituin={}".format(
            self.read_token(), self.read_gtk(),friend_qq, username)
        try:
            request_firend_url = requests.get(url, headers=self.headers, cookies=self.getCookie())
            json_data = json.loads(request_firend_url.text)
            return json_data['data']['profile']['city']
        except KeyError:
            print("空间主人设置了访问权限，您无法进行操作")


    def firend_permission(self, uin=None):
        qzonetoken = self.read_token()
        gtk = self.read_gtk()
        url = "https://mobile.qzone.qq.com/list?qzonetoken={}&g_tk={}&format=json&list_type=shuoshuo&action=0&res_uin={}&count=10".format(
            qzonetoken,gtk, uin)
        request_shuoshuo_first_url = requests.get(url, headers=self.headers, cookies=self.getCookie())
        json_data = json.loads(request_shuoshuo_first_url.text)
        try:
            feedskey = json_data['data']['vFeeds'][0]['comm']['feedskey']
            appid = json_data['data']['vFeeds'][0]['comm']['appid']
            url = "https://h5.qzone.qq.com/proxy/domain/g.qzone.qq.com/cgi-bin/friendshow/cgi_get_visitor_single?uin={}&appid={}&blogid={}&param={}&ref=qzfeeds&beginNum=1&num=24&g_tk={}&qzonetoken={}".format(
                uin, appid, feedskey, feedskey, gtk, qzonetoken)
            sad_see_request = requests.get(url, cookies=self.getCookie()).text
            jsdate = json.loads(sad_see_request[10:-3])
            if jsdate['message'] != 'succ':
                return 0
            else:
                return 1
        except KeyError:
            print("空间主人设置了访问权限，您无法进行操作")

    def get_sad_see(self, uin=None, appid=None, logid=None, starttime=None, stoptime=None):
        city1 = "昆明"
        city2 = "丽江"
        gtk = self.read_gtk()
        qzonetoken = self.read_token()
        sqlite = Sqlite()
        proxies = {
            'http': 'http://182.96.194.88',
            'https': 'https://1.199.192.143'
        }
        url = "https://h5.qzone.qq.com/proxy/domain/g.qzone.qq.com/cgi-bin/friendshow/cgi_get_visitor_single?uin={}&appid={}&blogid={}&param={}&ref=qzfeeds&beginNum=1&num=24&g_tk={}&qzonetoken={}".format(
            uin, appid, logid, logid, gtk, qzonetoken)
        sad_see_request = requests.get(url, cookies=self.getCookie()).text
        jsdate = json.loads(sad_see_request[10:-3])
        if jsdate['message'] == "请登录后再试":
            print("可能被冻结了....换号吧")
            with open("token_gtk_sid.txt", 'r') as f:
                data = json.load(f)
                qq = data['qq']
                Sqlite().del_cookie(qq)
            main()
            os._exit(1)
        elif jsdate['message'] == 'succ':
            print("开始爬取 '{}' 的说说 '{}'".format(uin,logid))
            Sqlite().del_undone_shuoshuo_key_and_sava_completed_shuoshuo_key(uin,logid)
            for date in range(len(jsdate['data']['list'])):
                if starttime == None and stoptime == None:
                    print("发布说说的QQ号: ", uin, "看了这条说说的QQ号:", jsdate['data']['list'][date]['uin'], '访问时间: ',datetime.fromtimestamp(jsdate['data']['list'][date]['time']), "用户名: ",jsdate['data']['list'][date]['name'])
                    if self.firend_permission(jsdate['data']['list'][date]['uin']) == 0:
                        print("QQ:{} 抱歉，由于对方设置，您没有权限查看这些访客，所以不存入数据库...".format(uin))
                    else:
                        if self.filter_data(jsdate['data']['list'][date]['uin']) == city1:
                            print("爬取到一个 {} 的用户,QQ '{}'".format(city1,jsdate['data']['list'][date]['uin']))
                            sqlite.sava_beijing_undone_qq_number_and_sava_information_qq_number(jsdate['data']['list'][date]['uin'])
                            print('{} 已保存到临时数据库中...'.format(jsdate['data']['list'][date]['uin']))
                        else:
                            print("得到QQ '{}',并保存到临时数据库中.....".format(jsdate['data']['list'][date]['uin']))
                            sqlite.sava_undone_qq_number_and_sava_information_qq_number(jsdate['data']['list'][date]['uin'])
                            print('{} 已保存到临时数据库中...'.format(jsdate['data']['list'][date]['uin']))
                elif str(starttime) <= str(datetime.fromtimestamp(jsdate['data']['list'][date]['time']))[0:4] and str(
                        stoptime) >= str(datetime.fromtimestamp(jsdate['data']['list'][date]['time']))[0:4]:
                    print("发布说说的QQ号: ", uin, "看了这条说说的QQ号:", jsdate['data']['list'][date]['uin'], '访问时间: ',datetime.fromtimestamp(jsdate['data']['list'][date]['time'], "用户名: ",jsdate['data']['list'][date]['name']))
                    if self.firend_permission(jsdate['data']['list'][date]['uin']) == 0:
                        print("QQ:{} 抱歉，由于对方设置，您没有权限查看这些访客，所以不存入数据库...".format(uin))
                    else:
                        if self.filter_data(jsdate['data']['list'][date]['uin']) == city1:
                            print("爬取到一个 {} 的用户,QQ '{}'".format(city1,jsdate['data']['list'][date]['uin']))
                            sqlite.sava_beijing_undone_qq_number_and_sava_information_qq_number(jsdate['data']['list'][date]['uin'])
                            print('{} 已保存到临时数据库中...'.format(jsdate['data']['list'][date]['uin']))
                        else:
                            sqlite.sava_undone_qq_number_and_sava_information_qq_number(jsdate['data']['list'][date]['uin'])
                            print("得到QQ '{}',并保存到临时数据库中.....".format(jsdate['data']['list'][date]['uin']))
                else:
                    pass  # 方便扩展~
        else:
            print("QQ:{} 抱歉，由于对方设置，您没有权限查看这些访客".format(uin))


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
    del_cookie()

def del_cookie():
    with open("token_gtk_sid.txt",'r') as f:
        data = json.load(f)
        qq = data['qq']
        cookie = data['cookie']
        gtk = data['gtk']
        sid = data['sid']
        qzonetoken = data['qzonetoken']
        Sqlite().del_cookie(qq)
        Sqlite().sava_cookie_and_args(qq,cookie,gtk,sid,qzonetoken)

def main():
    # sqlite = Sqlite()
    qq_see = QQ_number()
    get_total_number = Sqlite().read_20_shuoshuo_key()
    while get_total_number:
        dicts = []
        get_total_number = Sqlite().read_20_shuoshuo_key()
        for i in get_total_number:
            # qq_see.get_sad_see(i[0], i[1], i[2])
            t = threading.Thread(target=qq_see.get_sad_see,args=(i[0],i[1],i[2]))
            dicts.append(t)

        for x in dicts:
            x.setDaemon(True)
            x.start()
        x.join()
        change_cookie()


if __name__ == '__main__':
    main()
    # del_cookie()
    # del_cookie()
    # change_cookie()
    # s = QQ_number()
    # print(s.getCookie())