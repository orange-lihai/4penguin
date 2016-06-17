#! /usr/bin/python
#! -*- encoding: utf-8 -*-

import utils
import os
BASE_DIR = os.path.dirname(__file__)
LOG_DIR = os.path.join(BASE_DIR, '../logs/')

def log2file(log_str):
    with open(name = LOG_DIR + "http_log_" + utils.timestr4suffix(), mode = 'w', buffering = 1024) as f:
        f.write(log_str)
        f.flush()
        
if "__main__" == __name__:
    log2file("-------------------------------------")