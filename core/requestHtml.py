import requests
from requests_html import HTMLSession
from url_cons import login_url

# 设置请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/54.0.2840.99 Safari/537.36"}


def initRequest():
    bd_html = requests.get(login_url, params="", headers=headers)
    if bd_html.status_code == 200:
        print(bd_html.text)
        pass
    else:
        print("请求失败了")
        pass


def initRequestSession():
    # 1. 创建session对象，可以保存Cookie值
    ssion = requests.session()
    # 2. 处理 headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
    # 3. 需要登录的用户名和密码
    data = {"email": "mr_mao_hacker@163.com", "password": "alarmchime"}

    # 4. 发送附带用户名和密码的请求，并获取登录后的Cookie值，保存在ssion里
    ssion.post("http://www.renren.com/PLogin.do", data=data, headers=headers)
    # 5. ssion包含用户登录后的Cookie值，可以直接访问那些登录后才可以访问的页面
    response = ssion.get("http://www.renren.com/410043129/profile")

    # 6. 打印响应内容
    print
    response.text
