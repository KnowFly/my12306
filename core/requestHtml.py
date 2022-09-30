# import requests
from requests_html import HTMLSession
import json
from url_cons import login_url

# 设置请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/54.0.2840.99 Safari/537.36"}

def initRequestSession():
    # 3. 需要登录的用户名和密码
    data = {"username": "17600000000", "appid": "otn"}
    sson = HTMLSession()
    my12306 = sson.post('https://kyfw.12306.cn/passport/web/checkLoginVerify/', data=data,headers=headers)
    if my12306.status_code == 200:
        print("返回数据" + my12306.text)
        # python原始数据
        print("python串" + (repr(my12306.json())))
        # 转换成json字符串
        jsonStr = json.dumps(my12306.json())
        print("json字符串" + jsonStr)
        # 转化Json字典
        jsonMap = json.loads(jsonStr)
        # 获取字典Value
        print(jsonMap['login_check_code'])
    else:
        print("获取验证码失败")
