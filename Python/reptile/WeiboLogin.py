import requests
import base64
import rsa
import re
import json
import binascii

class WeiBoLogin(object):

    def __init__(self):
        self.request = requests.Session()
        self.username = ""      # 用户名
        self.password = ""    # 密码
        self.information = {}
        self.headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"}

    def baseUsername(self):
        su = base64.b64encode(bytes(self.username, encoding="utf-8")).decode("utf-8")
        return su
    
    def rsaPassword(self, **kw):
        serevrtime, nonce, rsakv, pubkey = kw['servertime'], kw['nonce'], kw['rsakv'], kw['pubkey']
        # 'RSAKey.setPublic(me.rsaPubkey,"10001");password=RSAKey.encrypt([me.servertime,me.nonce].join("\\t")+"\\n"+password)'  # 原js加密 
        pw_string = "\t".join([str(serevrtime), nonce]) + '\n' + self.password
        key = rsa.PublicKey(int(pubkey, 16), 65537)
        pw_encrypt = rsa.encrypt(pw_string.encode("utf-8"), key)
        sp = binascii.b2a_hex(pw_encrypt)
        self.password = ""    # 清空密码
        return sp

    def getPrelogin(self, *args):
        re_preloginCallBack = re.compile('sinaSSOController.preloginCallBack(.*)')
        url = "https://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su={}&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.19)&_=1577269910313".format(args[0])
        responses = self.request.get(url, headers=self.headers)
        re_responses = json.loads(re_preloginCallBack.search(responses.text).group(1)[1:-1])
        return re_responses

    def login(self, *args, **kw):
        location_replace = re.compile('location.replace(.*)')
        userdomain = re.compile('"userdomain":"(.*)"')
        re_uid = re.compile("CONFIG\['uid'\]='.*?';")      # id号
        re_nick = re.compile("CONFIG\['nick'\]='.*?';")    # 用户名
        re_sex = re.compile("CONFIG\['sex'\]='.*?';")      # 性别
        re_watermark = re.compile("CONFIG\['watermark'\]='.*?';")    # 主页域名
        url = "https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.19)"
        post_data = {
			'entry': 'weibo',
			'gateway': '1',
			'from': '',
			'savestate': '7',
			'qrcode_flag': 'false',
			'useticket': '1',
			"pagerefer":"http://passport.weibo.com/visitor/visitor?entry=miniblog&a=enter&url=http%3A%2F%2Fweibo.com%2F&domain=.weibo.com&ua=php-sso_sdk_client-0.6.14",
			'vsnf': '1',
			'su': args[0],
			'service':'miniblog',
			'servertime': kw["servertime"],
			'nonce': kw["nonce"],
			'pwencode': 'rsa2',
			'rsakv': kw["rsakv"],
			'sp': args[1],
			'sr': '1920 * 1080',
			'ncoding': 'UTF - 8',
			'prelt': '912',
			'url': "http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack",
			'returntype': 'META'
		}

        post_request = self.request.post(url, headers=self.headers, data=post_data).content.decode("GBK")    # 第一层重定向！
        get_location_replace_url = location_replace.search(post_request).group(1)[2:-3]
        get_location_replace_request = self.request.get(get_location_replace_url, headers=self.headers).content.decode("GBK")    # 第二层重定向!！
        if location_replace.search(get_location_replace_request) == None:
            print("账号或者密码有误")
        else:
            get_location_replace_url2 = location_replace.search(get_location_replace_request).group(1)[2:-7]
            get_location_replace_request2 = self.request.get(get_location_replace_url2, headers=self.headers).content.decode("GBK")    # 第三层重定向！！！
            get_userdomain_url = "http://weibo.com/" + userdomain.search(get_location_replace_request2).group(1)
            get_home = self.request.get(get_userdomain_url, headers=self.headers).content.decode("utf-8")
            uid = re_uid.search(get_home).group().split("=")[1][1:-2]
            nick = re_nick.search(get_home).group().split("=")[1][1:-2]
            sex = re_sex.search(get_home).group().split("=")[1][1:-2]
            watermark = re_watermark.search(get_home).group().split("=")[1][1:-2]
            self.information['uid'] = uid
            self.information['nick'] = nick
            self.information['sex'] = sex
            self.information['watermark'] = watermark

    def printInformation(self, **kw):
        print("登录成功!\nid: {}\nusername: {}\nsex: {}\nwatermark: {}".format(kw['uid'], kw['nick'], kw['sex'], kw['watermark']))

    def main(self):
        username = self.baseUsername()
        prelogin = self.getPrelogin(username)
        password = self.rsaPassword(**prelogin)
        self.login(username, password, **prelogin)
        self.printInformation(**self.information)

if __name__ == "__main__":
    login = WeiBoLogin()
    login.main()