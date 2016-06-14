import requests
from bs4 import BeautifulSoup as BS

session = requests.Session()
headers = {}

url = 'http://news.baidu.com/ns?ct=0&rn=20&ie=utf-8&bs=%E7%99%BE%E5%BA%A6&rsv_bp=1&sr=0&cl=2&f=3&prevct=no&tn=news&word=%E5%8C%97%E6%B1%BD+EU260&rsv_n=2&rsv_sug3=1&rsv_sug4=36&rsv_sug1=1&rsp=0&inputT=674&rsv_sug=1'
req = session.get(url = url, headers = headers)
bsObj = BS(req.txt)
