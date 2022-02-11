#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# *********************************************************************************************
#    file_scan.py
# ------------------
#  Uwe Berger; 2021
#
# ...scan mp3-Files and insert mp3-tag-infos in a sqlite3-table...
#                                                  -------
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

import my_sql
import sqlite3
import mp3_tags

mp3_dir = '/datadisk/mp3'

# ************************************************************************************
def find_files(dirs=[], extensions=[]):
    global file_count, error_count
    new_dirs = []
    for d in dirs:
        try:
            new_dirs += [os.path.join(d, f) for f in os.listdir(d)]
        except OSError:
            if os.path.splitext(d)[1] in extensions:
                #files.append(d)
                file_count = file_count + 1
                f = mp3_tags.get_mp3_infos(d)
                sql = my_sql.get_insert_sql(my_sql.mp3_collection_struct, f, my_sql.tab_mp3_collection)
                try:
                    cur.execute(sql)
                except sqlite3.Error as er:
                    print(f['file_name'])
                    print(er)
                    print(sql)
                    print("*************************************")
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
db=sqlite3.connect(my_sql.db_file)
cur = db.cursor()

sql = my_sql.get_create_sql(my_sql.mp3_collection_struct, my_sql.tab_mp3_collection)
cur.execute(sql)

files = []
file_count = 0
error_count = 0
find_files(dirs=[mp3_dir], extensions=['.mp3'])

print(F"Files: {file_count}; Errors: {error_count}")


db.commit()

db.close()
exit()