#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# *********************************************************************************************
# file_scan_mysql.py
# ------------------
#  Uwe Berger; 2021
#
# ...scan mp3-Files and insert mp3-tag-infos in a mysql-table...
#                                                  -----
#
# see also for scan mp3-tags:
#   https://stackoverflow.com/questions/24841191/get-mp3-play-time-using-eye3d-with-python
#
# ---------
# Have fun!
#
# *********************************************************************************************

import os
import time

import eyed3
from eyed3 import id3
from eyed3 import load

import my_mysql
import mp3_tags

import pymysql

mp3_dir = '/datadisk/mp3'

# ************************************************************************************
def find_files(dirs=[], extensions=[]):
    global file_count
    new_dirs = []
    for d in dirs:
        try:
            new_dirs += [os.path.join(d, f) for f in os.listdir(d)]
        except OSError:
            if os.path.splitext(d)[1] in extensions:
                file_count = file_count + 1
                f = mp3_tags.get_mp3_infos(d)
                sql = my_mysql.get_insert_sql(my_mysql.mp3_collection_struct, f, my_mysql.tab_mp3_collection)
                cur.execute(sql)
                if (file_count%100) == 0:
                    print(F"...{file_count} files scanned...")
                    db.commit()
    if new_dirs:
        find_files(new_dirs, extensions )
    else:
        return


# ************************************************************************************
# ************************************************************************************
# ************************************************************************************

eyed3.log.setLevel("ERROR")

# ******************************************************************
# ******************************************************************
# ******************************************************************

db = pymysql.connect(host='dockerpi', user='xxxx', password='yyyy', database='mp3_collection')

cur = db.cursor()

# create table if not exists
sql = my_mysql.get_create_sql(my_mysql.mp3_collection_struct, my_mysql.tab_mp3_collection)
cur.execute(sql)
db.commit()

# scan files
files = []
file_count = 0
find_files(dirs=[mp3_dir], extensions=['.mp3'])

# result of file scan
print(F"Files: {file_count} scanned.")

db.commit()
db.close()
print('Exit!!!')
exit()