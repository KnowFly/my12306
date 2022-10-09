# import requests
from requests_html import HTMLSession
import json
from url_cons import login_url

# 设置请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/54.0.2840.99 Safari/537.36"}


def initRequestSession():
    # 域名/robots.txt 查看协议
    # 需要登录的用户名和密码
    data = {"username": "17600000000", "appid": "otn", "slideMode": "1"}
    sson = HTMLSession()
    my12306 = sson.post('https://kyfw.12306.cn/passport/web/checkLoginVerify/', headers=headers, data=data)
    if my12306.status_code == 200:
        print("获取验证码成功")
        # response.text 获取字符串类型的响应正文：
        # response.content 获取bytes类型的响应正文：
        # response.json()  直接将响应内容的json字符串转换成python的list或者dict

        # json_str = json.dumps(json_data)  # 返回值为json字符串
        # json.loads(json_str)  # 返回值为python的list或者dict

        json_data = my12306.json()
        json_str = my12306.text
        json_content = my12306.content

        print("json字符串" + json_str)  # {"result_message":"","login_check_code":"1","result_code":0}
        print("============================================")
        print(json_content)  # b'{"result_message":"","login_check_code":"1","result_code":0}'
        print("============================================")
        print(json_data)  # {'result_message': '', 'login_check_code': '1', 'result_code': 0}
        print("============================================")
        print(type(json_str))  # <class 'str'>
        print("============================================")
        print(type(json_data))  # <class 'dict'>
        print("============================================")
        login_check_code = json_data['login_check_code']
        print(login_check_code)
        print("============================================")
        json_str = json.dumps(json_data)
        print(json_str)  # {"result_message": "", "login_check_code": "1", "result_code": 0}
        print("============================================")
        # 转化Json字典
        json_map = json.loads(json_str)
        # 获取字典Value
        print(json_map['login_check_code'])
        # 写入Json文件
        fp = open('./12306_main.json', 'w', encoding='utf-8')  # 创建⽂件
        json.dump(json_data, fp=fp, ensure_ascii=False)
        # 写入html文件
        with open("12306_main.html", mode="w", encoding="utf-8") as f:  # 创建⽂件
            f.write(json_str)  # 保存在⽂件中
    else:
        print("获取验证码失败")
