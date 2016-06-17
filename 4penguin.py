#! /usr/bin/python
#! -*- encoding: utf-8 -*-

import sys
sys.path.append("..")

from spiders import baidu_news

if "__main__" == __name__:
    baidu_news.do(param = {'word': '北汽 EU260', 'pn': 0, 'rn': 50})
