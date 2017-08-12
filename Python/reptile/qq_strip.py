import requests
import json
import numpy
import time

cookie = "welcomeflash=1473018671_15; qz_pv=2; qz_greater_than_5s=2; 1473018671_todaycount=2; 1473018671_totalcount=1232100; RK=Ql3HQKL+an; __Q_w_s_hat_seed=1; __Q_w_s__QZN_TodoMsgCnt=1; eas_sid=C1O5S0w1j9w8g8h6X4v8w8r9U6; pgv_pvid=6833249281; pgv_pvi=542381056; ptui_loginuin=1473018671; pgv_info=ssid=s6181913278; ptisp=ctc; ptcz=95e93c56d969137f5fc07f61b7a438cbe4b03269370ffd35dae79654d86d910a; pt2gguin=o1473018671; uin=o1473018671; skey=@yYsfzd9FI; p_uin=o1473018671; p_skey=kA2Xhov2EWNmPIfKvZbRk8NvrvW-KOLXYZsEB0zDcps_; pt4_token=MDwO5lVgXcM7lmzjWF-sdhhgNBmI-yCJ1FyeO2CpPt8_; Loading=Yes; qzspeedup=sdch; qqmusic_uin=1473018671; qqmusic_key=@yYsfzd9FI; qqmusic_fromtag=6; qqmusic_vkey=8A627A1C2743E75B4815A044386703A6BDCB8D11CEC5CBBA8E408D5979E72AF09B3A0C814A99C88F2365845F3946BD640CB7751C82F2B64C; qqmusic_guid=1473018671; qzmusicplayer=qzone_player_1473018671_1502453482691; qz_screen=1920x1080; QZ_FE_WEBP_SUPPORT=1; cpu_performance_v8=70"
url = "https://user.qzone.qq.com/1473018671/infocenter"
header = {
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
'Connection': 'keep-alive',
'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Cookie': cookie}
proxies = {'http':'http://27.185.194.55:8118'}
# urls = "https://h5.qzone.qq.com/proxy/domain/m.qzone.qq.com/cgi-bin/new/get_msgb?uin=1473018671&hostUin=1473018671&start=0&s={}&format=jsonp&num=10&inCharset=utf-8&outCharset=utf-8&g_tk=1041315152&qzonetoken=6e76d19a3ada11087aacf450ca3f81ddc04bd3cade83579e58c53575bbaaf183bef18ab65fc3feccde9607".format(numpy.random.random())
urlse = "https://h5.qzone.qq.com/proxy/domain/m.qzone.qq.com/cgi-bin/new/get_msgb?uin=1473018671&hostUin=1473018671&num=0&start=0&hostword=0&essence=1&r={}&iNotice=0&inCharset=utf-8&outCharset=utf-8&format=jsonp&ref=qzone&g_tk=1041315152&qzonetoken=6e76d19a3ada11087aacf450ca3f81ddc04bd3cade83579e58c53575bbaaf183bef18ab65fc3feccde9607".format(numpy.random.random())
rs = requests.get(urlse,headers=header,proxies=proxies)
js = json.loads(rs.text[10:-3])
get_total = js['data']['total']
for i in range(0,get_total,10):
	time.sleep(numpy.random.random())
	url = "https://h5.qzone.qq.com/proxy/domain/m.qzone.qq.com/cgi-bin/new/get_msgb?uin=1473018671&hostUin=1473018671&num={}&start={}&hostword=0&essence=1&r={}&iNotice=0&inCharset=utf-8&outCharset=utf-8&format=jsonp&ref=qzone&g_tk=1041315152&qzonetoken=6e76d19a3ada11087aacf450ca3f81ddc04bd3cade83579e58c53575bbaaf183bef18ab65fc3feccde9607".format(i,i,numpy.random.random())
	r = requests.get(url, headers=header,proxies=proxies)
	jstext = json.loads(r.text[10:-3])
	print("··········第 {} 个···········".format(i))
	for x in range(len(jstext['data']['commentList'])):
		print("留言者:",jstext['data']['commentList'][x]['nickname'],"内容:",jstext['data']['commentList'][x]['htmlContent'])