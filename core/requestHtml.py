# import requests
from requests_html import HTMLSession
from url_cons import login_url

# 设置请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/54.0.2840.99 Safari/537.36"}


# def initRequest():
#     bd_html = requests.get(login_url, params="", headers=headers)
#     if bd_html.status_code == 200:
#         print(bd_html.text)
#         pass
#     else:
#         print("请求失败了")
#         pass


def initRequestSession():
    ssion = HTMLSession
    # 2. 处理 headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
    # 3. 需要登录的用户名和密码
    data = {"email": "mr_mao_hacker@163.com", "password": "alarmchime"}
    session = HTMLSession()
    # 往京东主页发送get请求
    jd = session.get('https://jd.com/')
    # 得到京东主页所有的链接，返回的是一个set集合
    print(jd.html.links)
    print('*' * 1000)
    # 若获取的链接中有相对路径，我们还可以通过absolute_links获取所有绝对链接
    print(jd.html.absolute_links)
