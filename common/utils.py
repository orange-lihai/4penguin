#! /usr/bin/python
#! -*- encoding: utf-8 -*-

import datetime, time, os
from glob import glob
# '%Y-%m-%d %H:%M:%S'
import xlwt

BASE_DIR = os.path.dirname(__file__)
LOG_DIR = os.path.join(BASE_DIR, '../logs/')

def timestr4suffix():
    return time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime(time.time()))

def time2str(f = '%Y-%m-%d %H:%M:%S', d = None):
    if d == None: d = time.localtime(time.time())
    return time.strftime(f, d)

def removefiles(patten_str):
    try:
        os.remove(glob(patten_str))
    except:
        pass

def save2excel(file_name = 'rs.xls', sheet_name = 'sheet1', rs = [], header_attrs = []):
    file_name = LOG_DIR + file_name
    wb = xlwt.Workbook(encoding='utf8')
    sheet = wb.add_sheet(sheetname = sheet_name, cell_overwrite_ok = True)   
    for i in range(len(rs)):
        c = rs[i]
        for j in range(len(header_attrs)):
            h = header_attrs[j]
            if i == 0: sheet.write(i, j, h['v'])        
            sheet.write(i + 1, j, c[h['k']])        

    removefiles(file_name)    
    wb.save(file_name)            

# 判断一个字符串是否是时间字符串, 比如: 2016年06月16日, 8小时前, 5分钟前 等等.
def istimestr(s):
    if s is None: return False
    idx = s.find(u'年')
    if idx > 0 and s[idx - 1:idx].isdigit(): return True
    idx = s.find(u'月')
    if idx > 0 and s[idx - 1:idx].isdigit(): return True    
    idx = s.find(u'日')
    if idx > 0 and s[idx - 1:idx].isdigit(): return True 
    idx = s.find(u'时')
    if idx > 0 and s[idx - 1:idx].isdigit(): return True
    idx = s.find(u'分')
    if idx > 0 and s[idx - 1:idx].isdigit(): return True
    idx = s.find(u'秒')
    if idx > 0 and s[idx - 1:idx].isdigit(): return True
    idx = s.find(u'天')
    if idx > 0 and s[idx - 1:idx].isdigit(): return True
    idx = s.find(u'小时')
    if idx > 0 and s[idx - 1:idx].isdigit(): return True
    idx = s.find(u'分钟')
    if idx > 0 and s[idx - 1:idx].isdigit(): return True    
    return False
    
if "__main__" == __name__:
    print timestr4suffix()
    print time2str()
    save2excel(rs=[{'a': 'xxxxxx', 'b': 111}, {'a': 'yyyyy', 'b': '90888'}], header_attrs = [{'k': 'a', 'v': '我们'}, {'k': 'b', 'v': 'cccc'}])
    print istimestr(u'杭州日报')