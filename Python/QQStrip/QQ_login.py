import requests
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities, ActionChains
from selenium.common.exceptions import NoSuchElementException, WebDriverException
import webbrowser
import time
from bs4 import BeautifulSoup
import re
import pickle
from urllib import request
import json
from mysqlite import MySqlite

class Sqlite(MySqlite):

    def __init__(self):
        MySqlite.__init__(self)


class qzone_login():
    def __init__(self, username,password):
        self.username = username
        self.password = password
        # self.sqlite = MySqlite()
        self.headers = {
            "user-agent": "Mozilla/5.0 (Linux; U; Android 2.3.6; zh-cn; GT-S5660 Build/GINGERBREAD) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1 MicroMessenger/4.5.255"}
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = (
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
            '*/*',
            'en-US,en;q=0.8',
            'max-age=0',
            'keep-alive'

        )
        self.browser = webdriver.PhantomJS(desired_capabilities=dcap, executable_path=r'phantomjs-2.1.1-windows/bin/phantomjs.exe')
        # self.browsers = webdriver.Chrome(desired_capabilities=dcap,executable_path=)
        self.browser.set_window_size(480, 500)
        self.browser.get("https://mobile.qzone.qq.com")
        print("Start!")

    def save_screens(self):
        self.browser.get('https://mobile.qzone.qq.com')
        self.browser.save_screenshot('ceshi5.png')

    # 需要验证
    # 1.打开手机QQ安全中心，查看动态验证码
    # 2.使用短信验证(暂时未搞~)
    def fuck_verify_code(self):
        Bs = BeautifulSoup(self.browser.page_source, 'lxml')
        # print(self.browser.page_source)
        try:
            try:
                # print(self.browser.page_source)
                Bfind = Bs.find('iframe')['src']  # 获取动态验证码的页面url
                self.browser.get(Bfind)
            except TypeError:
                print("这个验证码可能会出现无法获取的情况,请关闭程序重启运行，会尽快解决！！！Sorry~")
        except WebDriverException:
            print("这个验证码可能会出现无法获取的情况,请关闭程序重启运行，会尽快解决！！！Sorry~")
            # self.reboot_verify_code()
        time.sleep(2)
        token_code = self.browser.find_element_by_xpath('//*[@id="token_code"]')
        btn = self.browser.find_element_by_xpath('//*[@id="scroller"]/div[2]/form/div[1]/button')
        verify_code = input("动态验证码: ")  # 输入动态码
        verify_code_action = ActionChains(self.browser)
        verify_code_action.move_to_element(token_code).click().send_keys(verify_code)
        verify_code_action.move_to_element(btn).click()
        verify_code_action.perform()
        time.sleep(5)
        # self.browser.save_screenshot('ceshi4.png')
        print("登陆成功!,正在保存cookie....")
        cookie = {}
        for c in self.browser.get_cookies():
            cookie[c['name']] = c['value']
        self.sava_cookie(self.username, cookie)

        print("OVER")

    #  识别图标的验证
    def reboot_verify_code(self):
        time.sleep(3)
        check_url = "https://ssl.ptlogin2.qq.com/check?pt_tea=2&uin={}&appid=549000929&ptlang=2052&regmaster=&pt_uistyle=9&r=0.14612517165842842&pt_jstoken=3507970968".format(self.username)
        check_request = requests.get(check_url,headers=self.headers).text
        cap_cd = check_request.split(",")[1][1:-1]
        cap_union_prehandle_url = "https://ssl.captcha.qq.com/cap_union_prehandle?aid=549000929&captype=&protocol=https&clientype=1&disturblevel=&apptype=2&noheader=0&color=&showtype=&fb=1&theme=&lang=2052&cap_cd={}&uid={}&callback=_aq_65462&sess=".format(cap_cd,self.username)
        cap_union_prehandle_req = requests.get(cap_union_prehandle_url,headers=self.headers).text
        js_cap = json.loads(cap_union_prehandle_req.split('(')[1][0:-1])
        print(js_cap['sess'])
        cap_union_new_show_url = "https://ssl.captcha.qq.com/cap_union_new_show?aid=549000929&captype=&protocol=https&clientype=1&disturblevel=&apptype=2&noheader=0&color=&showtype=&fb=1&theme=&lang=2052&sess={}&fwidth=0&uid={}&cap_cd={}&rnd=857672".format(js_cap['sess'],self.username,cap_cd)
        s = webbrowser.open(cap_union_new_show_url)
        self.browser.save_screenshot("ceshi.png")



    def sava_cookie(self, cookies):
        file = open('cookie.txt', 'wb')
        json_pickle = pickle.dump(cookies, file)
        file.close()

    def getCookie(self):
        try:
            with open("cookie.txt", 'rb') as f:
                cookie = pickle.load(f)
            return cookie
        except EOFError:
            pass

    # 获取qzonetoken
    def get_qzonetoken(self, cookie):
        url = "https://user.qzone.qq.com/" + self.username
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"}
        request_url = requests.get(url, headers=headers, cookies=cookie).text
        BS = BeautifulSoup(request_url, 'lxml')
        Bfind = BS.find_all('script', type="text/javascript")[-1]
        pattern = re.compile(r'{ try{return ".*?";}')
        with open('token_gtk_sid.txt', 'r') as tgs_r:
            token_gtk_sid = json.load(tgs_r)
        try:
            for br in Bfind:
                token_gtk_sid['qzonetoken'] = pattern.findall(br)[0].split(" ")[2][1:-3]
                with open('token_gtk_sid.txt', 'w') as tgs:
                    json.dump(token_gtk_sid, tgs)
        except IndexError:
            print("网速不好....无法获取qzone~")

    def read_token(self):
        with open('token_gtk_sid.txt', 'r') as rt:
            return json.load(rt)['qzonetoken']

    def read_gtk(self):
        with open('token_gtk_sid.txt') as rt:
            return json.load(rt)['gtk']

    def read_sid(self):
        with open('token_gtk_sid.txt', 'r') as rt:
            return json.load(rt)['sid']

    # 生成g_tk
    def get_gtk(self, cookie):
        with open('token_gtk_sid.txt', 'r') as tgs_r:
            token_gtk_sid = json.load(tgs_r)
            tgs_r.close()
        hashes = 5381
        for g in cookie['p_skey']:
            hashes += (hashes << 5) + ord(g)
            token_gtk_sid['gtk'] = hashes & 0x7fffffff
        with open('token_gtk_sid.txt', 'w') as tgs_w:
            json.dump(token_gtk_sid, tgs_w)
            tgs_w.close()
            # return hashes & 0x7fffffff

    # 获取sid
    def get_sid(self, text):
        with open("token_gtk_sid.txt", 'r') as tgs_r:
            token_gtk_sid = json.load(tgs_r)
            tgs_r.close()
        try:
            Bs = BeautifulSoup(text, 'lxml')
            bfind = Bs.find_all("script", type="application/javascript")
            pattern = re.compile(r'window.g_App = {"sid":".*?",')
            for i in bfind[1]:
                with open('token_gtk_sid.txt', 'w') as tgs_w:
                    token_gtk_sid['sid'] = pattern.findall(i)[0].split(':')[1][1:-2]
                    json.dump(token_gtk_sid, tgs_w)
                    tgs_w.close()
        except IndexError:
            print("网速不好....无法获取sid~")

    def login(self):
        print("正在登录......")
        u = self.browser.find_element_by_xpath('//*[@id="u"]')
        p = self.browser.find_element_by_xpath('//*[@id="p"]')
        go = self.browser.find_element_by_xpath('//*[@id="go"]')
        u.clear()  # 清空账号输入框的内容
        action = ActionChains(self.browser)  # 模拟键盘输入
        action.move_to_element(u).click().send_keys(self.username)  # 移动到账号输入框并选中，然后输入账号
        action.move_to_element(p).click().send_keys(self.password)  # 移动到密码输入框并选中，然后输入密码
        action.move_by_offset(go.location['x'], go.location['y'])
        action.click(go)
        action.perform()
        time.sleep(3)
        # self.browser.save_screenshot('ceshi1.png')
        if self.browser.title != "QQ空间":
            print("需要验证~验证码的格式已经改变~现无法用以前的方法")
            print("建议先手动在登陆一下~或者再运行一次~")
            # self.save_screens()
            # self.fuck_verify_code()
        else:
            print("登陆成功!,正在保存cookie....")
            cookie = {}
            for c in self.browser.get_cookies():
                cookie[c['name']] = c['value']
            self.sava_cookie(cookie)
            self.get_qzonetoken(self.getCookie())
            self.get_gtk(self.getCookie())
            self.get_sid(self.browser.page_source)
            Sqlite().sava_cookie_and_args(self.username, json.dumps(self.getCookie()), self.read_gtk(), self.read_sid(),self.read_token())
            print("{} 的cookie已保存!".format(self.username))
            cookies = Sqlite().read_cookie()
            cookie_and_args = {}
            cookie_and_args['qq'] = cookies[0]
            cookie_and_args['cookie'] = cookies[1]
            cookie_and_args['gtk'] = cookies[2]
            cookie_and_args['sid'] = cookies[3]
            cookie_and_args['qzonetoken'] = cookies[4]
            with open("token_gtk_sid.txt", 'w') as tgs:
                json.dump(cookie_and_args, tgs)


    def __del__(self):
        self.browser.quit()

def get_login_qq_number():
    name = ""
    pw = ""
    print("获取账号和密码......")
    with open('myQQ.txt', 'r') as f:
        number = f.read().strip()
    username_pw = number.split('\n')
    for i in username_pw:
        print("---------------------------------")
        username = i.split('\n')[0].split(" ")[0]
        password = i.split('\n')[0].split(" ")[1]
        print("获取QQ： '{}'".format(username))
        qq = qzone_login(username,password)
        qq.login()
        # print(qq.read_gtk(),qq.read_sid(),qq.read_token(),qq.getCookie())

def change_cookie():
    pass

if __name__ == '__main__':
    get_login_qq_number()
