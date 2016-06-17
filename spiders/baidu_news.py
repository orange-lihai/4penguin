#! /usr/bin/python
#! -*- encoding: utf-8 -*-

import sys
sys.path.append("..")
import requests
import urllib
import time
import bs4
from bs4 import BeautifulSoup as BS
from common import utils
from common.log2file import log2file

COMMON_URL = 'http://news.baidu.com/ns?cl=2&ct=0&tn=news&ie=utf-8&bt=0&et=0'
def get_response(param = {}):
    session = requests.Session()
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36"
               , "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
               , "Accept-Encoding": "gzip, deflate, sdch"
               , "Accept-Language": "zh-CN,zh;q=0.8"
               , "Host": "news.baidu.com"
               , "Connection": "keep-alive"
               , "Referrer": "https://www.baidu.com/"
               , "Cookie": "BAIDUID=D12212AE45CC06F404FA886E1CD9A33C:FG=1; BIDUPSID=D12212AE45CC06F404FA886E1CD9A33C; PSTM=1456125295; MCITY=-233%3A131%3A; LOCALGX=%u5317%u4EAC%7C%30%7C%u5317%u4EAC%7C%30; Hm_lvt_e9e114d958ea263de46e080563e254c4=1465778781,1465809868,1465865928,1465866238; Hm_lpvt_e9e114d958ea263de46e080563e254c4=1465866238; pgv_pvi=1921624064; pgv_si=s6728900608; BDRCVFR[C0p6oIjvx-c]=mk3SLVN4HKm; BD_CK_SAM=1; BDSVRTM=220; H_PS_PSSID="
               }
    url = COMMON_URL + "&" + "&".join( [k + '=' + urllib.quote(str(v)) for k, v in param.items()] )
    print ' --- --- --- : ' + url
    req = session.get(url = url, headers = headers)
    if req is not None:
        if req.status_code == 200: 
            bsObj = BS(req.text, "html.parser")
            # log response text to a file
            # log2file(bsObj.prettify(encoding='utf8', formatter='minimal'))        
        return req.status_code, bsObj
    else:
        return -1, None

def extract_param_append(param, bsObj):
    pages = bsObj.find_all(name = 'span', attrs = {'class': 'pc'})
    return [
        {'word': param['word'], 'pn': param['rn'] * (int(pc.text) - 1), 'rn': param['rn']} 
        for pc in pages 
        if int(pc.text) > 1
    ]

def extract_records(param, bsObj):
    xs = []
    rs = bsObj.find_all(name = 'div', attrs = {'class': 'result', 'id': True})
    for r in rs:
        x = {'href': '', 'title': '', 'site': '', 'time': '', 'info': '', 'same_news_num': '', 'kw': ''}
        # 获得标题和链接
        _title = r.find(name = 'a', attrs = {'data-click': True})
        x['href'] = _title['href']
        x['title'] = _title.text
        _content = r.find(name = 'div', attrs = {'class': ['c-span18', 'c-span-last']})
        if _content is None: 
            _content = r.find(name = 'div', attrs = {'class': ['c-summary', 'c-row']})
        if _content is None:
            xs.append(x)
            continue
        
        # 获得来源网站, 时间, 摘要, 相同新闻数量
        for ch in _content.children:
            if ch.name == 'p' and ch['class'][0] == 'c-author':
                au = ch.prettify(formatter=lambda s: s.replace(u'\xa0', ' '))
                au_arr = BS(au, "html.parser").text.replace(u'\n', '').split(' ')
                au_arr = [a for a in au_arr if len(a) > 0]
                if utils.istimestr(au_arr[0]):
                    x['time'] = au_arr[0]
                else:
                    x['site'] = au_arr[0]
                    if len(au_arr) >= 2: x['time'] = au_arr[1]
            elif ch.name == 'span' and ch['class'][0] == 'c-info':
                _more_link = ch.find(name = 'a', attrs = {'class': 'c-more_link'})
                if _more_link is not None: x['same_news_num'] = _more_link.text
                x['same_news_num'] = ''.join( [n for n in x['same_news_num'][:] if n.isdigit()] )
                if x['same_news_num'].isdigit(): x['same_news_num'] = int( x['same_news_num'] )
                break
            else:
                if type(ch) == bs4.element.NavigableString:
                    x['info'] +=  unicode(ch.string)
                else:
                    x['info'] +=  ch.text
        xs.append(x)
    print ' --- --- --- : ' + str(len(xs))
    return xs

def do(param = {}):
    print ' begin ----------------------- at: ' + utils.time2str()
    rs = []
    param_append = []
    status_code, bsObj = get_response(param = param)
    if status_code == 200:
        param_append = extract_param_append(param, bsObj) 
        rs.extend( extract_records(param, bsObj) )
        # just get first page        
        # param_append = []
        for k in param_append:
            status_code, bsObj = get_response(param = k)
            if status_code == 200:
                rs.extend( extract_records(k, bsObj) )
            else:
                print ' --- --- --- : ' + status_code
            time.sleep(0.2)
    else:
        print ' --- --- --- : ' + status_code
    if len(rs) >= 1:
        rs[0]['kw'] = param['word']
    print rs
    print len(rs)
    file_name = 'baidu_news_'+ param['word'].decode('utf8') +'_rs.xls'
    header_attrs =  [{'k': 'kw', 'v': '车型'}, 
                   {'k': 'site', 'v': '媒体'}, 
                   {'k': 'time', 'v': '时间'}, 
                   {'k': 'title', 'v': '标题'}, 
                   {'k': 'href', 'v': '链接'}, 
                   {'k': 'same_news_num', 'v': '相关信息条数'}, 
                   {'k': 'info', 'v': '摘要'}
                   ]
    utils.save2excel(file_name = file_name, sheet_name = 'sheet1', rs = rs, header_attrs = header_attrs)
    print ' end   ----------------------- at: ' + utils.time2str()

if "__main__" == __name__:
    param = {'word': '北汽 EU260', 'pn': 0, 'rn': 50}
    do(param = param)
    
    