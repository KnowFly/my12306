# import requests
import base64
import threading
import time

from requests_html import HTMLSession
import json
from PIL import Image  # 操作图片
from url_cons import login_url
import time

# session会话对象，请求和返回的信息保存在session中
sson = HTMLSession()
sson.verify = False

# import threading

# 设置请求头
header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:94.0) Gecko/20100101 Firefox/94.0",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Referer": "https://exservice.12306.cn/"
}


def get(url, headers):
    reqs = sson.get(url, headers=headers)
    reqs.encoding = 'UTF-8-SIG'
    return reqs.text


def post(url, headers, data):
    reqs = sson.post(url, headers=headers, data=data)
    reqs.encoding = 'UTF-8-SIG'
    return reqs


def getQR():
    # 域名/robots.txt 查看协议
    # 需要登录的用户名和密码
    data = {"appid": "otn"}
    my12306 = post('https://kyfw.12306.cn/passport/web/create-qr64', headers=header,
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
        if result_code == '0':
            print("获取验证码成功==>" + json_data['image'])
            image_base64 = getImage(base64.b64decode(json_data['image']))
            Image.open(image_base64).show()  # 依赖PIL库，打开图片(会创建一个零食文件打开图片，图片未被占用时销毁)
            # threading.Thread.start(checkQR(uuid))  # 开一个线程去执行监听
            checkQR(uuid)
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
        # cookies = sson.cookies
        checkqr = sson.post('https://kyfw.12306.cn/passport/web/checkqr', headers=header, data=data)
        json_result = checkqr.json()
        print(json_result)
        result_code = json_result['result_code']
        if '1' == result_code:
            print('已扫描请确定')
        elif result_code == "2":
            # {'result_message': '扫码登录成功', 'uamtk': 'geflkK0exvF4FpW7AetzKv-ukhmd1gVMTDPHyLlsrpo64d1d0', 'result_code': '2'}
            print('扫码登录成功')
            uamtk = json_result['uamtk']
            checkUamtk(uamtk)
            return
        elif result_code == "3":
            getQR()
            print('二维码已过期')
            return
        time.sleep(2)


def checkUamtk(uamtk):
    data = {"appid": "excater", "uamtk": uamtk}
    checkqr = sson.post('https://kyfw.12306.cn/passport/web/auth/uamtk', headers=header,
                        data=data)
    json_result = checkqr.json()
    print(json_result)
    result_code = json_result['result_code']
    result_message = json_result['result_message']
    apptk = json_result['apptk']
    newapptk = json_result['newapptk']
    if 0 == result_code:
        # {'apptk': None, 'result_message': '验证通过', 'result_code': 0, 'newapptk': 'uyXy9uCNi0IqjX35O4d-EKM_yLx5QPlH8iBh6Zv-jY0wed1d0'}
        print('auth检验成功')
        checkUamauthclient(newapptk)
        return
    elif 1 == result_code:
        if checkLogin():
            print("已登陆查询票")
            pass
        else:
            print("未登陆成功")
            pass
        return
    else:
        print('auth检验失败')
        return


def saveCookie():
    # _cookies = sson.cookies.get_dict()
    # # 取到session的cookie信息 取出来是键值对把他转化成字符串类型保存下来
    # cookieStr = json.dumps(_cookies)
    # with open('./cookies.txt', 'w') as f:
    #     f.write(cookieStr)
    #     print('记录cookie成功')
    pass


def getCookie():
    # try:
    # with open('./cookies.txt', 'r') as f:
    #     _cookie = json.load(f)
    #     print(_cookie)
    #     sson.cookies = _cookie
    #     session的cookie是一个RequestsCookieJar类型的，把键值对转换为给他
    #     sson.cookies = requests.utils.cookiejar_from_dict(_cookie)
    # except FileNotFoundError:
    #     print('还未登陆过..')
    pass


def checkUamauthclient(tk):
    data = {"tk": tk}
    checkqr = sson.post('https://exservice.12306.cn/excater/uamauthclient', headers=header,
                        data=data)
    json_result = checkqr.json()
    # {'apptk': 'uyXy9uCNi0IqjX35O4d-EKM_yLx5QPlH8iBh6Zv-jY0wed1d0', 'result_message': '验证通过', 'result_code': 0, 'username': '张飞'}
    print(json_result)
    result_code = json_result['result_code']
    if 0 == result_code:
        print('登陆成功')
        saveCookie()
        if checkLogin():
            print("已登陆查询票")
            pass
        else:
            print("未登陆成功")
            pass
        return
    else:
        print('checkUamauthclient失败')


def checkLogin():
    data = {}
    getCookie()
    checkqr = sson.post('https://exservice.12306.cn/excater/login/checkLogin', headers=header,
                        data=data)
    json_result = checkqr.json()
    # {'data': {'flag': '0', 'isCanMember': False, 'time': 1666863616015}, 'status': True, 'errorMsg': ''}
    print(json_result)
    if (json_result['status']):
        if (json_result['data']['flag']):
            return json_result['data']['flag']
        else:
            return
    return False


def queryTeket():
    # https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc&fs=%E5%8C%97%E4%BA%AC,BJP&ts=%E5%A4%AA%E5%8E%9F,TYV&date=2022-10-28&flag=N,Y,Y
    # 车类型
    linktypeid = "dc"
    # 出发地
    fs = "北京,BJP"
    # 目的地
    ts = "太原,TYV"
    # 出发日期
    date = "2022-10-28"
    # flag = N, Y, Y
    # {"httpstatus":200,"data":{"result":["PJVi7rEr00ZX06Kid40awJfLqeVAdulyrLLDDs2t0eBjPAKvTfWqdrjXfLWY3ytvtmBGH0cJ6aQn%0Ae5DlDBVwvbgibsoBuHV80TBkO6D5emqIWNX4QgPy5pZyBMyp2zx%2BTvbLGBU04dJlzSdlL9tjJPoS%0AwOfAEU7fFfrz1AddkZhvrL0QUUiaRvQH64DC4hP4J4mKCTmM%2FYBHC2LNkNIV0V4zMm%2F9TFY93lCW%0AdmXO4OD4fdu%2BzIBtMktvfbdUzKkvV2%2F1OoxHq1mnC5ZFCm%2F8NiYm0DC6Ltqc0F3fvS52REq2e20D%0AI5Fte%2Fy9l9PkCGpp|预订|240000G62310|G623|FTP|ABV|FTP|TNV|08:13|11:21|03:08|Y|4Vzkll7%2FVD9RIw0I%2F8T5AMIro%2BJF4wcfdkwkIw3J7WZ5cKIs|20221028|3|P3|01|05|1|0|||||||||||有|8|无||O0M090|OM9|1|1||O021050021M0337000089068900000|0|||||1|0#1#0#0#z||","a5uO%2FCPIvdHWmQKNnj0UItpgoQ9v8jyM42HDo8A%2FMKRoL3ODidSf%2FT4W8sEmcY1gNkovhNYP39n1%0ACmh%2BWTYPZT9EW%2Bx3IfI2fLEguAenjrsjYLh1WwBWaau1UrL8YJtUW8LBN21KQsQDxZTrDMV7%2FKcv%0ARDg4ThQ9wugyeOzk2GYYEx2E653wZo%2BYNYQbrvCl%2F5Hq3Lh54gOkC%2FA%2BeDR7BTDRmfOkdbB3JB9H%0AdNa%2FKGziqUSlC9B8OEC2rs%2FkujTL0TsdSiEmlQUdsE97gIRaCx080gTkSmA3vpe%2FQbvYC69m9nDZ%0A%2FRsXxg5y7yi2DKdw|预订|240000G6050F|G605|FTP|TNV|FTP|TNV|11:26|14:10|02:44|Y|2J5gtpNma95%2BdhVO2tPeXNS0gzY0bC5DboxaJ9ifRkqrpKvY|20221028|3|P4|01|04|1|0|||||||||||有|8|无||M0O090|MO9|1|1||M031600008O0197500219061200000|0|||||1|0#0#0#0#z||","NYdcza5wweKSHuKK8xv3Q6jE5ZgXcH7RSpFz2xmhT%2FceSd0GkFiqxP%2BSvWeCFalmiWfW2Z%2BdGQ7l%0A5TkeH%2B7Ytj6%2FoMivNTv2MmReGsh%2BKtJq7R%2FXPOgDJ1yxwLmhUpZRYwx5uxY5Gvdw41mlzIBxL8wU%0A3UhPM%2FDcOADWCQ35JEJJVSA1dwUi4vHVIkWFvdLjp7SoPAsdAq5rEmm1I0eNXoDd0T%2BFxYOodqxu%0AuW8jib%2FMBQGz8EPUnfPTwTmqlXAtuCWktqL8sp%2BAMFai5Fd92LINisv6MUCkpg0R%2FWksFfOSKGfl%0ACqhLhHR7OJrA6l04|预订|240000G6070C|G607|FTP|TNV|FTP|TNV|11:31|14:27|02:56|Y|ol6hpcsElIpLo9u0%2FxdOL0NX1tC465LnWLbwkHhQChRTpK42|20221028|3|P3|01|05|1|0|||||||||||有|12|1||O090M0|O9M|1|0||O0184500219061200001M029600012|0|||||1|0#0#0#0#z||","Jif1cIrMU3Sj7OZf%2BOuR9jvQD%2FEa%2B8BS2amRVYIBKW%2B0vewH493KvhMoqBdKqDGH%2FEaf8a9yXa9v%0AZ6JTQzcl4JDBviF2jAGYqWoqxyB4ey8dfrf4%2FfZzDYJdqo0ir7%2FeHXYK0ZlgwsxXVhtwbPKJqLxg%0AURC4YkuSFjsn4IEhJ96p3dsuY7LnctfQ3VAmDk5bux83KtH0Os42heLeF9YI9ntNJuKgRzM0m9xA%0A8fk%2BB1g7fjMj%2B3TlQOcCGa2ubrB1O5gbddyBVQ15%2Fd0K61hPbbx74M6SnOlqnQUr0lLlwvgMUtjq%0AQW7YCfY6bxPEJsFI8uuaiQ%3D%3D|预订|2400000T4111|T41|BXP|XAY|BXP|TYV|14:22|19:46|05:24|Y|PY9iJNUXg3cFCUIRxSSybyXD0NoyWMme50fWSDs4vG1lNyoDuy0w%2BgrWaHY%3D|20221028|3|P2|01|04|1|0||||有|||无||有|有|||||301040W0|3141|1|0||3012900021100720002140197000211007203000|0|||||1|#0#0#0#z||","Xu7rl%2FyxoSQ7khP9nKeUdoP29tJ16caVPIimgqXjyTs79hRburqe%2FKDEaPyqnhmYt9oS2yp%2Bdxsu%0AxVcN4V3Sbbdg7SQJQjCPiyrm3MTHmMB9umxNVcULEM%2FYZe4nL1jJ5KyhdAos9sugDmjeNe8N5Ten%0Ap1jXYR3hWD56AzHvyroNUP4Nl4G7ZQ%2FHXIfzlF9kttVEAIe7qD%2FprEdWlYARSniLHusLnpvPeFN6%0ANY32ViJYXQ1LwvX8I3Ixcxv9dCDLVjWCT%2B692NfJOaV%2Bo%2BGS0jwdkQcZaa6mHREpfP3eyn1KgLzx%0A4aWWxUPpbMW0Iam5|预订|240000G6270L|G627|FTP|ABV|FTP|TNV|14:29|17:30|03:01|Y|N7tgTjEAUzhHYBG%2Ff40YLkrbHhZoFUSqtKSi6sREMytz0IKq|20221028|3|P3|01|06|1|0|||||||||||有|无|无||O090M0|O9M|0|1||O0197500219061200000M031600000|0|||||1|0#0#0#0#z||","KG88tsdzT2dyCXN9TVGZ4uUpH2JyTvowqY%2FJ%2Bt1xPKGqJOTio1a2LRHpmqlThWkxZb01NCXxtW3s%0AcabC7xxj5ibii3%2FzzAwJAYViH8kc%2Fg8sUIjqlVXAugUP477uhZXpgYJwczjblZIMa5zajQxkymAD%0AnfgZNUl5Ax8rnvFXPHTfu1sXhYawtOlru25MqMjH8pFu2Wlvn34xIVeooCxdDeuCQQDDrDjmPvkv%0AxwghNe1wbVLe%2F3UhFbS3P6gpLB%2B0UOWMZxDOn24LAXzE8oCvbhH6YQ9vjtsWMXa5ll3rj6SVrNAq%0A7MLvFupWWRv0te4v|预订|240000G62909|G629|FTP|ABV|FTP|TNV|17:30|20:36|03:06|Y|pe0lucJvr9%2Bvv78BancKfo6Ke%2FYiHOyUGKZ63dFiJ1RajIib|20221028|3|P4|01|06|1|0|||||||||||有|10|1||O0M090|OM9|0|0||O019050021M0305000109059050001|0|||||1|0#0#0#0#z||","Tosk2p60EzOlmVjMHssorWlXOl7O8usBoscHJ2G98%2FQ1XzOz2AOSBX%2B1GIVEa52LzmitxAGBMNV6%0AEPOQ2DEvoWqZQAW6d11SrTbKdZMQC9eQ%2B%2BuI2P89XobQt%2Fa06RKNLazNpGxgs1gAirRD7fHno1wQ%0Aoe39Mokd%2B2y0RCSbNH8JUvVb9Iaa81nk%2F4Rdb8J6dd0LMtm9dn42H31%2FScZzRUdup5xBumPmOYik%0AOAwV2CPg6G5rtTyInEQ25WIlKq4rjXOY6oSkMLetSdXb0eRZbdb2K65qb0jO91PrgNKNMA9gNPlV%0A%2Basgdc0s7lfW19KP|预订|240000G6130J|G613|FTP|TNV|FTP|TNV|18:48|21:52|03:04|Y|jg4ESUU%2FkGcCVPLUUgw7SXnFbB6%2FVww2GGqkIm7e8wxrKJ6z|20221028|3|P3|01|05|1|0|||||||||||有|9|无||90O0M0|9OM|1|1||9059050000O016350021M026300009|0|||||1|0#0#0#0#z||","vUgPY%2FP9re2d2x1DqE56VuUBmm4%2FMzmGd9eE3psJkI7KReonv3vcCFEMImIO8ph5NW6jrB%2FcMdLF%0AxUGYBtCmaR1QWgbgE9zbLtLYqnWq%2BiQlW7g6ox7yXFR9FVNmIPKweHLUnAPwEwR97wdFQZnqY9Ug%0ADNqWywEktTRnLiSv0gYeZht5AKJ6%2BWnVJNvcf0sr%2Byn5DFIX1gGxMxeUeXbM3EDP5s01rIIsTN7F%0A8OqmBLf5wNBrzhrayHn4DASEElLnAX4%2F9eyc1WNhPkfEDdYIK8%2F3BQ%2FDe3WKpCaLOtcObdKyF8JJ%0AudhoLOaYBcAPx3xOlnJUtoXfKc9WeQlD|预订|240000Z2770C|Z277|BXP|YIJ|BXP|TYV|20:03|00:28|04:25|Y|sk29skf6bq1Fz%2BAcfWSTNziCIPpOY3HrQZ175MRn86A1mO3U4qGtVYqmVxidsvxe3pwlDtqhcME%3D|20221028|3|P3|01|03|1|0||12||有|||无||有|10|||||40306010W0|43611|1|0||40197000213012900021603580001210072000101007203000|0|||||1|#0#0#0#z||"],"flag":"1","map":{"TYV":"太原","FTP":"北京丰台","BXP":"北京西","TNV":"太原南"}},"messages":"","status":true}
    "https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc&fs=%E5%8C%97%E4%BA%AC,BJP&ts=%E5%A4%AA%E5%8E%9F,TYV&date=2022-10-28&flag=N,Y,Y"
    pass
