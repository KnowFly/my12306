# import requests
import base64
import time

from requests_html import HTMLSession
import json
from PIL import Image  # 操作图片
from url_cons import login_url

# 设置请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/54.0.2840.99 Safari/537.36"}


def getQR():
    # 域名/robots.txt 查看协议
    # 需要登录的用户名和密码
    data = {"appid": "otn"}
    sson = HTMLSession()
    cookies = sson.cookies
    # my12306 = sson.post('https://kyfw.12306.cn/passport/web/checkLoginVerify/', cookies=cookies, headers=headers,
    my12306 = sson.post('https://kyfw.12306.cn/passport/web/create-qr64', cookies=cookies, headers=headers,
                        # my12306 = sson.post('https://kyfw.12306.cn/passport/web/checkqr', cookies=cookies, headers=headers,
                        data=data)
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
        # login_check_code = json_data['login_check_code']
        # print(login_check_code)
        print("============================================")
        json_str = json.dumps(json_data)
        print(json_str)  # {"result_message": "", "login_check_code": "1", "result_code": 0}
        print("============================================")
        # 转化Json字典
        # json_map = json.loads(json_str)
        # 获取字典Value
        # print(json_map['login_check_code'])

        # 写入Json文件
        # fp = open('./12306_main.json', 'w', encoding='utf-8')  # 创建⽂件
        # json.dump(json_data, fp=fp, ensure_ascii=False)
        # # 写入html文件
        # with open("12306_main.html", mode="w", encoding="utf-8") as f:  # 创建⽂件
        #     f.write(json_str)  # 保存在⽂件中
        print("============================================")
        result_code = json_data['result_code']
        uuid = json_data['uuid']
        checkQR(uuid)
        if result_code == '0':
            print(json_data['image'])
            image_base64 = getImage(base64.b64decode(json_data['image']))
            Image.open(image_base64).show()  # 依赖PIL库，打开图片(会创建一个零食文件打开图片，图片未被占用时销毁)
        else:
            print("获取二维码图片失败")
    else:
        print("获取验证码失败")


def getImage(img):
    filepath = './12306_login.jpg'
    with open(filepath, 'wb') as fd:  # w写入 b二进制形式
        fd.write(img)
    return filepath


def checkQR(uuid):
    while True:
        data = {"appid": "otn", "uuid": uuid}
        sson = HTMLSession()
        cookies = sson.cookies
        checkqr = sson.post('https://kyfw.12306.cn/passport/web/checkqr', cookies=cookies, headers=headers, data=data)
        json_result = checkqr.json()
        print(json_result)
        status_code = json_result['result_code']
        print(status_code)
        print("============================================" + status_code)
        if '1' == status_code:
            print('已扫描请确定')
            return
        elif status_code == "2":
            print(json_result['result_message'])
        elif status_code == "3":
            print('二维码过期')
            getQR()
            return
        time.sleep(2)
