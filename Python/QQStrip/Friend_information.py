import json
import pickle
import requests
from mysqlite import MySqlite
import pymysql


class Mysql():

    def __init__(self):
        self.connent_sql = pymysql.connect(user='root',
                      password="crazyrookie",
                      host="127.0.0.1",
                      port=3306,
                      charset="utf8mb4")
        self.cursor = self.connent_sql.cursor()

        sql = """
        CREATE DATABASE IF NOT EXISTS information DEFAULT CHARACTER SET utf8mb4;
        USE information;
        CREATE TABLE IF NOT EXISTS firend_information(
            uin VARCHAR(11) UNIQUE,
            nickname VARCHAR(88),
            gender VARCHAR(2) DEFAULT " ",
            age VARCHAR(3) DEFAULT " ",
            city VARCHAR(10) DEFAULT " ",
            country VARCHAR(20) DEFAULT " "
            
        );
        """

        self.cursor.execute(sql)
        self.connent_sql.commit()


    def sava_information(self,uin,nickname,gender,age,city,country):
        try:
            sql = "INSERT INTO firend_information (uin,nickname,gender,age,city,country) VALUES ('{}','{}','{}','{}','{}','{}');".format(uin,nickname,gender,age,city,country)
            self.cursor.execute(sql)
            self.connent_sql.commit()

        except pymysql.err.IntegrityError:
            pass

class Sqlite(MySqlite):

    def __init__(self):
        MySqlite.__init__(self)

class Information():

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
        try:
            with open("cookie.txt", 'rb') as f:
                cookie = pickle.load(f)
            return cookie
        except EOFError:
            pass

    def get_login_qq_number(self):
        with open('myQQ.txt', 'r') as f:
            number = f.read().strip()
        name = number.split('\n')[0].split(" ")[0]
        return name

    def get_firend_qzone_date(self, firend_qq=''):
        print("开始获取 '{}' 的信息".format(firend_qq))
        username = self.get_login_qq_number()
        url = "https://h5.qzone.qq.com/webapp/json/friendSetting/getMainPage?qzonetoken={}&g_tk={}&uin={}&visituin={}".format(self.read_token(), self.read_gtk(),firend_qq, username)
        request_firend_url = requests.get(url, headers=self.headers, cookies=self.getCookie())
        json_data = json.loads(request_firend_url.text)
        try:
            print(
                '浏览者QQ: ', json_data['data']['profile']['uin'],
                "昵称: ", json_data['data']['profile']['nickname'],
                "性别: ", json_data['data']['profile']['gender'],
                "年龄: ", json_data['data']['profile']['age'],
                "城市: ", json_data['data']['profile']['city'],
                "国家: ", json_data['data']['profile']['country'],
            )
            # Mysql().sava_information(json_data['data']['profile']['uin'],
                                 # json_data['data']['profile']['nickname'],
                                 # json_data['data']['profile']['gender'],
                                 # json_data['data']['profile']['age'],
                                 # json_data['data']['profile']['city'],
                                 # json_data['data']['profile']['country'])
            Sqlite().del_information_qq_number(firend_qq)
        except KeyError:
            print("空间主人设置了访问权限，您无法进行操作")

def main(information):
    # information_qq = Sqlite().read_information_number()
    # while information_qq:
    #   n = 1
    information_qq = Sqlite().read_information_number()
    while information_qq:
        information_qq = Sqlite().read_information_number()
        if information_qq == []:
            print("QQ号没啦~请继续获取~")
        else:
            for num in information_qq:
                information.get_firend_qzone_date(num[0])




if __name__ == '__main__':
    information = Information()
    main(information)