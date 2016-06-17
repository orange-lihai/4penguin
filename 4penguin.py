#! /usr/bin/python
#! -*- encoding: utf-8 -*-

import sys
sys.path.append("..")

from spiders import baidu_news

if "__main__" == __name__:
    baidu_news.do()
