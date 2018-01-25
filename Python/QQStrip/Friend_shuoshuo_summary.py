import requests
import json
import pickle
from mysqlite import MySqlite
import pymongo


class Mymongodb():

    def __init__(self):
        self.conn = pymongo.MongoClient('127.0.0.1',27017)
        self.db = self.conn['qq']

    def inserts(self,nick,uin,createtime,msg,content):
        coll = self.db['summary']
        document = {"nick":nick,'uin':uin,'createtime':createtime,'msg':msg,'content':content}
        indo = coll.insert(document)
        print(document)


class Sqlite(MySqlite):

    def __init__(self):
        MySqlite.__init__(self)

class Shuoshuo_summary():

    def __init__(self):
        self.headers = {"user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36"}

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
        try:
            with open("cookie.txt", 'rb') as f:
                cookie = pickle.load(f)
            return cookie
        except EOFError:
            pass

    def summary(self,uin,feedkey):
        # 功能:
        # 爬取说说的内容保存至Mongodb~
        url = "https://user.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msgdetail_v6?uin={}&tid={}&t1_source=1&ftype=0&sort=0&pos=0&num=20&g_tk={}&callback=_preloadCallback&code_version=1&format=jsonp&need_private_comment=1&qzonetoken={}&g_tk={}".format(uin,feedkey,self.read_gtk(),self.read_token(),self.read_gtk())
        requrl = requests.get(url,headers=self.headers).text
        split_json = json.loads(requrl.split("_preloadCallback(")[1][0:-2])
        Sqlite().del_undone_summary_key_and_sava_completed_summary_key(uin,feedkey)
        # Sqlite().del_undone_shuoshuo_key_and_sava_completed_shuoshuo_key(uin, feedkey)
        if split_json['code'] == -10031:
            print("对不起,主人设置了保密,您没有权限查看~",'用户名: {}, QQ: {}, 个性签名: {}, 此说说的发布时间: {}'.format(split_json['usrinfo']['name'],split_json['usrinfo']['uin'],split_json['usrinfo']["msg"],split_json['usrinfo']['createTime']))
        if split_json['code'] == -10029:
            print("该条内容已被删除","用户名: {}, QQ: {}, 个性签名: {}".format(split_json['usrinfo']['name'],split_json['usrinfo']['uin'],split_json['usrinfo']['msg']))
        else:
            try:
                if split_json['conlist'] == None:
                    print("用户名: {},QQ: {},发布时间: {},个性签名: {}\n说说内容: \n{}".format(split_json['usrinfo']['name'],split_json['usrinfo']['uin'],split_json['usrinfo']['createTime'],split_json['usrinfo']['msg'],split_json['content']))
                    Mymongodb().inserts(split_json['usrinfo']['name'],split_json['usrinfo']['uin'],split_json['usrinfo']['createTime'],split_json['usrinfo']['msg'],split_json['content'])
                    if split_json['content'] == "":
                        print("用户名: {},QQ: {},发布时间: {},个性签名: {}\n说说内容: \n{}".format(split_json['usrinfo']['name'],split_json['usrinfo']['uin'],split_json['usrinfo']['createTime'],split_json['usrinfo']['msg'],split_json['rt_con']['conlist'][0]['con']))
                    Mymongodb().inserts(split_json['usrinfo']['name'], split_json['usrinfo']['uin'],
                                      split_json['usrinfo']['createTime'], split_json['usrinfo']['msg'],
                                      split_json['content'])

                else:
                    print("用户名: {},QQ: {},发布时间: {},个性签名: {}\n说说内容: \n{}".format(split_json['usrinfo']['name'],split_json['usrinfo']['uin'],split_json['usrinfo']['createTime'],split_json['usrinfo']['msg'],split_json['conlist'][0]['con']))
                Mymongodb().inserts(split_json['usrinfo']['name'], split_json['usrinfo']['uin'],
                                  split_json['usrinfo']['createTime'], split_json['usrinfo']['msg'],
                                  split_json['content'])
            except KeyError:
                pass
            except TypeError:
                pass


    def main(self):
        feedkey = Sqlite().read_10_summary_key()
        while feedkey:
            feedkey = Sqlite().read_10_summary_key()
            if feedkey == []:
                print("说说已爬取完成~请运行Friend_shuoshuo_key获取一些说说key吧~")
            for i in feedkey:
                self.summary(i[0],i[1])

if __name__ == '__main__':
    Summary = Shuoshuo_summary()
    Summary.main()