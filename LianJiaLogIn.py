# -*- coding: utf-8 -*-
"""
@author: zachary
"""
import json
from http import cookiejar
import re
import zlib
import urllib
import urllib.request


#获取Cookiejar对象（存在本机的cookie消息）
cookie = cookiejar.CookieJar()
#自定义opener,并将opener跟CookieJar对象绑定
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie))
#安装opener,此后调用urlopen()时都会使用安装过的opener对象
urllib.request.install_opener(opener)


home_url = 'http://bj.lianjia.com/'
auth_url = 'https://passport.lianjia.com/cas/login?service=http%3A%2F%2Fbj.lianjia.com%2F'
chengjiao_url = 'http://bj.lianjia.com/chengjiao/'
 
 
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': 'passport.lianjia.com',
    'Pragma': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36'
}

# 获取lianjia_uuid
req = urllib.request.Request('http://bj.lianjia.com/')
opener.open(req)
# 初始化表单
req = urllib.request.Request(auth_url, headers=headers)
result = opener.open(req)


# 获取cookie和lt值
pattern = re.compile(r'JSESSIONID=(.*)')
#pattern = re.compile(r'lianjia_ssid=(.*)')
jsessionid = pattern.findall(result.getheader('Set-Cookie').split(';')[0])[0]

html_content = result.read()
gzipped = result.getheader('Content-Encoding')
if gzipped:
    html_content = zlib.decompress(html_content, 16+zlib.MAX_WBITS)
pattern = re.compile(r'value="(LT-.*)" />')
lt = pattern.findall(str(html_content))[0]
pattern = re.compile(r'name="execution" value=\"(.*)\" ')
execution = pattern.findall(str(html_content))[0]
 

# data
data = {
    'username': '15210351799', #替换为自己账户的用户名
    'password': 'zzg19880415', #替换为自己账户的密码
    'execution': execution,
    '_eventId': 'submit',
    'lt': lt,
    'verifyCode': '',
    'redirect': '',
}

# urllib进行编码
post_data=urllib.parse.urlencode(data).encode(encoding='UTF8')


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': 'passport.lianjia.com',
    'Origin': 'https://passport.lianjia.com',
    'Pragma': 'no-cache',
    'Referer': 'https://passport.lianjia.com/cas/login?service=http%3A%2F%2Fbj.lianjia.com%2F',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
    'Upgrade-Insecure-Requests': '1',
    'X-Requested-With': 'XMLHttpRequest',
}
 

req = urllib.request.Request(auth_url, post_data, headers)


try:
    result = opener.open(req)
except urllib.request.HTTPError as e:
    print(e.getcode())
    print(e.reason)
    print(e.geturl())
    print(e.info())
    req = urllib.request.Request(e.geturl())
    result = opener.open(req)
    req = urllib.request.Request(chengjiao_url)
    result = opener.open(req).read()
    # print(result)