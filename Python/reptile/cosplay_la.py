# -*- utf-8 -*-

import requests
import json
from bs4 import BeautifulSoup

class CosPlay:

    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1)"
                                      " AppleWebKit/537.36 (KHTML, like Gecko)"
                                      " Chrome/65.0.3325.181 Safari/537.36"}
        # URL地址说明:
        #   从关注度开始，默认排行的粉丝太少了
        #   如果要修改的话:
        #       0-0-0-0-0-   默认排行
        #       0-0-0-0-1-   关注度
        #       0-0-0-0-2-   最新加入
        #       0-0-0-0-3-   获赞数
        #       0-0-0-0-4-   活跃度
        # 还可以根据城市来~更改url就ok了~比如北京的:110000-0-0-0-1- 要改的话可以在网页里抓~
        self.url = "http://cosplay.la/coser/index/0-0-0-0-1-"
        self.session = requests.session()    # 保持会话

    # 获取每页所有用户的主页链接
    def getUserHomeUrl(self, page):
        url = self.url + str(page)
        urlList = []
        respones = self.session.get(url, headers=self.headers).text
        bsoup = BeautifulSoup(respones, 'lxml')
        bfind_home_url = bsoup.find('div', class_='coser').find_all('a', class_='blue line')
        for bhu in bfind_home_url:
            urlList.append(bhu['href'])
        return urlList

    # 获取共计多少页
    def getPageTotalNum(self):
        pageNumResponse = self.session.get(self.url + '1', headers=self.headers).text
        pageNumBsoup = BeautifulSoup(pageNumResponse, 'lxml')
        bfindPageTotalNum = pageNumBsoup.find('div', class_="pagen tcenter mbottom20 font16").find_all('a')[-2]
        return bfindPageTotalNum.get_text().strip()

    # 获取用户的信息[名字, 地址, 年龄, 性别, 个性签名, 粉丝量, 关注量, 认证资料, 所在社团+社团链接, 主页地址, uid]
    def getUserInformation(self, userHomeUrl):
        userInformationsdict = {}
        userInformationResponse = self.session.get(userHomeUrl)
        bsoup = BeautifulSoup(userInformationResponse.text, 'lxml')
        if userInformationResponse.status_code == 200:    # 这里判断状态码是否为200,因为部分用户已经不存在啦~
            userName = bsoup.find('span', class_="bigname yahei white mright10 fleft").get_text()    # 用户名
            city = bsoup.find('span', class_="city greyc mright20 ").get_text()    # 地址
            if bsoup.find('span', class_="mright") == None: age = "保密"
            else: age = bsoup.find('span', class_="mright").get_text()    # 年龄
            if bsoup.find('span', class_="icon_boy") == None: gender = 'girl'    # 性别
            else: gender='boy'
            if bsoup.find('p', class_="mtop5 pink").get_text() == "": signature = "此用户没有写个性签名"    # 个性签名
            else: signature = bsoup.find('p', class_="mtop5 pink").get_text()
            fansCount = bsoup.find('a', id='FansCount').get_text()    # 粉丝量
            focusCount = bsoup.find('a', id='FocusCount').get_text()    # 关注量
            if bsoup.find('p', class_="padding5 gray font14") == None: certificationInformation = "不是认证用户"    # 认证资料
            else: certificationInformation = bsoup.find('p', class_="padding5 gray font14").get_text().strip()
            if bsoup.find('a', class_="fright mright blue font14 line mtop3") == None: society="此用户没有加入社团"    # 所在社团+社团链接
            else: society = bsoup.find('a', class_="fright mright blue font14 line mtop3")['href']+' & '+bsoup.find('a', class_="fright mright blue font14 line mtop3").get_text()
            homeUrl = bsoup.find('a', class_="red line")['href']    # 个人主页地址
            userid = bsoup.find('div', class_="usertop")['uid']   # uid, 如果没有这个东西,post的时候参数就会有问题~~
            userInformationsdict['userName'] = userName
            userInformationsdict['city'] = city
            userInformationsdict['age'] = age
            userInformationsdict['gender'] = gender
            userInformationsdict['signature'] = signature
            userInformationsdict['fansCount'] = fansCount
            userInformationsdict['focusCount'] = focusCount
            userInformationsdict['certificationInformation'] = certificationInformation
            userInformationsdict['society'] = society
            userInformationsdict['homeUrl'] = homeUrl
            userInformationsdict['uid'] = userid
            return userInformationsdict
        else:
            return "{} 此用户已经被删除啦~".format(userHomeUrl)

    # 用户的粉丝
    def userFansCount(self, userHomeUrl, uid):
        print("开始爬取 {} 的粉丝".format(userHomeUrl))
        num = 1
        while True:
            print("正在爬取第 '{}' 轮粉丝".format(num))
            postData = {
                'p': num,
                'action': 4,
                'uid': uid
            }
            fansPostResponse = json.loads(self.session.post(userHomeUrl + "/user/GetUserFriends", data=postData).text)
            if fansPostResponse['Data'] == []:
                print("'{}' 用户的粉丝已完, 共计 '{}' 个".format(userHomeUrl, num))
                break
            else:
                for fs in fansPostResponse['Data']:
                    fansInformation = self.getUserInformation("http://home.cosplay.la/"+fs['Domain'])
                    print(fansInformation)
            num += 1

    # 用户的关注
    def userFocusCount(self, userHomeUrl):
        pass

    def main(self):
        pageTotalNum = int(self.getPageTotalNum())
        num = 1
        print("共计", pageTotalNum)
        while pageTotalNum >= num:
            print("正在爬取第 '{}' 页".format(num))
            urlList = self.getUserHomeUrl(num)
            for ul in urlList:
                userInformations = self.getUserInformation(ul)
                print(self.userFansCount(ul, userInformations['uid']))
            print("第 '{}' 页爬取完成!".format(num))
            num += 1
        print("爬取完成!")

if __name__ == '__main__':
    cos = CosPlay()
    cos.main()