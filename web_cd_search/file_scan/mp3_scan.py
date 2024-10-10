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
# https://www.geeksforgeeks.org/retrieve-image-and-file-stored-as-a-blob-from-mysql-table-using-python/
# https://pynative.com/python-mysql-blob-insert-retrieve-file-image-as-a-blob-in-mysql/
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
import base64

import eyed3
from eyed3 import id3
from eyed3 import load

# ~ import mp3_tags

import pymysql

MP3_DIR = '/datadisk/mp3'
FOLDER_PICTURE = "folder.jpg"


# Tabelle mp3_collection
TAB_MP3_COLLECTION = 'mp3_collection'
MP3_COLLECTION_STRUCT = [
        {'col_name':'album',          'col_type':'varchar(255)',    'primary_key' : False},   
        {'col_name':'artist',         'col_type':'varchar(255)',    'primary_key' : False},   
        {'col_name':'album_artist',   'col_type':'varchar(255)',    'primary_key' : False},   
        {'col_name':'genre',          'col_type':'varchar(255)',    'primary_key' : False},   
        {'col_name':'title',          'col_type':'varchar(255)',    'primary_key' : False},   
        {'col_name':'year',           'col_type':'smallint(6)',     'primary_key' : False},   
        {'col_name':'track_nr',       'col_type':'smallint(6)',     'primary_key' : False},   
        {'col_name':'cd_id',          'col_type':'smallint(6)',     'primary_key' : False},   
        {'col_name':'sample_freq',    'col_type':'int(11)',         'primary_key' : False},   
        {'col_name':'bit_rate',       'col_type':'varchar(255)',    'primary_key' : False},   
        {'col_name':'mode',           'col_type':'varchar(255)',    'primary_key' : False},   
        {'col_name':'duration',       'col_type':'float',           'primary_key' : False},   
        {'col_name':'duration_str',   'col_type':'varchar(255)',    'primary_key' : False},   
        {'col_name':'file_name',      'col_type':'varchar(255)',    'primary_key' : True},   
        {'col_name':'path',           'col_type':'varchar(255)',    'primary_key' : False},   
        {'col_name':'file_size',      'col_type':'int(11)',         'primary_key' : False},   
        {'col_name':'file_modify',    'col_type':'varchar(255)',    'primary_key' : False},   
        {'col_name':'parser_error',   'col_type':'varchar(255)',    'primary_key' : False}
    ]

# Tabelle folder_picture
TAB_FOLDER_PICTURE = "folder_picture"
FOLDER_PICTURE_STRUCT = [
        {'col_name':'path',          'col_type':'varchar(255)',     'primary_key' : True},   
        {'col_name':'present',       'col_type':'varchar(255)',     'primary_key' : False},   
        {'col_name':'picture',       'col_type':'longblob',         'primary_key' : False},   
    ]


# ******************************************************************
def convert_str(s):
  s=s.replace("'","''")
  #s=s.replace('\x00','')
  return s

# ******************************************************************
def convertToBinaryData(filename):
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData

# ******************************************************************
def get_create_sql(struct, tab_name):
    comma = ''
    comma_pk = ''
    pk = ''
    s = f'create table if not exists {tab_name} ('
    for l in struct:
        s = s + f"{comma}{l['col_name']} {l['col_type']}"
        comma = ', '
        if l['primary_key']:
            pk = pk + f"{comma_pk}{l['col_name']}"
            comma_pk = ', '
    if len(pk) > 0:
        s = s + f", primary key ({pk})"
    s = s +')'
    return s
    
# ******************************************************************
def get_insert_sql(struct, values, tab_name):
    s = f'replace into {tab_name} values('
    comma = ''
    for l in struct:
        val = values[l['col_name']]
        if (isinstance(val, str) == True):
            apos = "'"
            val = convert_str(val)
        else:
            apos = ""
        s=s+f"{comma} {apos}{val}{apos}"
        comma = ','
    s = s +')'
    return s


# ************************************************************************************
def duration_sec2hour(s):
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return "{:02d}:{:02d}:{:02d}".format(int(h), int(m), int(s))
    

# ************************************************************************************
def get_mp3_infos(path):
    ret = {
            "artist"        : "None",
            "album"         : "None",
            "album_artist"  : "None",
            "genre"         : "None",
            "title"         : "None",
            "year"          : 0,
            "track_nr"      : 0,
            "cd_id"         : 0, #
            "sample_freq"   : 0,
            "bit_rate"      : "None",
            "mode"          : "None",
            "duration"      : 0,
            "duration_str"  : "None",
            "file_name"     : "None",
            "path"          : os.path.dirname(os.path.abspath(path)),
            "file_size"     : 0,
            "file_modify"   : "None",
            "parser_error"  : ""
    }
    tag = id3.Tag()
    tag.parse(path)
    a = load(path)
    try:
        ret["artist"] = str(tag.artist)
    except:
        ret["parser_error"] = F"{ret['parser_error']} artist"
    try:
        ret["album"] = str(tag.album)
    except:
        ret["parser_error"] = F"{ret['parser_error']} album"
    try:
        ret["album_artist"] = str(tag.album_artist)
    except:
        ret["parser_error"] = F"{ret['parser_error']} album_artist"
    try:
        ret["year"] = tag.recording_date.year
    except:
        ret["parser_error"] = F"{ret['parser_error']} year"
        pass
    try:
        ret["title"] = str(tag.title)
    except:
        ret["parser_error"] = F"{ret['parser_error']} title"
    try:
        ret["genre"] = str(tag.genre.name)
    except:
        ret["parser_error"] = F"{ret['parser_error']} genre"
        pass
    try:
        ret["track_nr"] = tag.track_num[0]
        if ret["track_nr"] == None: ret["track_nr"] = 0
    except:
        ret["parser_error"] = F"{ret['parser_error']} track_nr"
        pass
    try:
        ret["cd_id"] = tag.cd_id
        if ret["cd_id"] == None: ret["cd_id"] = 0
        if isinstance(ret["cd_id"], int) == False: ret["cd_id"] = 0
    except:
        ret["parser_error"] = F"{ret['parser_error']} cd_id"
        pass
    try:
        ret["file_modify"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(tag.file_info.mtime))
    except:
        ret["parser_error"] = F"{ret['parser_error']} mtime"
    try:
        ret["file_name"] = tag.file_info.name
    except:
        ret["file_name"] = path
        ret["parser_error"] = F"{ret['parser_error']} name"
    try:
        ret["sample_freq"] = a.info.sample_freq
    except:
        ret["parser_error"] = F"{ret['parser_error']} sample_freq"
    try:
        ret["bit_rate"] = a.info.bit_rate_str
    except:
        ret["parser_error"] = F"{ret['parser_error']} bit_rate"
    try:
        ret["mode"] = a.info.mode
    except:
        ret["parser_error"] = F"{ret['parser_error']} mode"
    try:
        ret["duration"] = a.info.time_secs
    except:
        ret["duration"] = 0
        ret["parser_error"] = F"{ret['parser_error']} duration"
    try:
        ret["duration_str"] = duration_sec2hour(a.info.time_secs)
    except:
        ret["duration_str"] = duration_sec2hour(0)
        ret["parser_error"] = F"{ret['parser_error']} duration_str"
    try:
        ret["file_size"] = a.info.size_bytes
    except:
        ret["parser_error"] = F"{ret['parser_error']} file_size"
    return ret


# ************************************************************************************
def find_files(dirs=[], extensions=[]):
    global file_count
    new_dirs = []
    for d in dirs:
        # folder.jpg
        if os.path.isfile(f"{d}/{FOLDER_PICTURE}"):
            picture = base64.b64encode(convertToBinaryData(f'{d}/{FOLDER_PICTURE}'))
            # ~ picture = convertToBinaryData(f'{d}/{FOLDER_PICTURE}')
            query = f"replace into {TAB_FOLDER_PICTURE} values(%s, %s, %s)"
            args = (d, "yes", picture)
            cur.execute(query, args)
        else:
            if os.path.isdir(f"{d}"):
                query = f"replace into {TAB_FOLDER_PICTURE} values(%s, %s, %s)"
                args = (d, "no", None)
                cur.execute(query, args)            
        # mp3-Dateien
        try:
            new_dirs += [os.path.join(d, f) for f in os.listdir(d)]
        except OSError:
            if os.path.splitext(d)[1] in extensions:
                file_count = file_count + 1
                # ~ f = get_mp3_infos(d)
                cur.execute(get_insert_sql(MP3_COLLECTION_STRUCT, get_mp3_infos(d), TAB_MP3_COLLECTION))
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

db = pymysql.connect(host='dockerpi', user='yyyy', password='xxxx', database='mp3_collection')

cur = db.cursor()

# create tables if not exists
cur.execute(get_create_sql(MP3_COLLECTION_STRUCT, TAB_MP3_COLLECTION))
cur.execute(get_create_sql(FOLDER_PICTURE_STRUCT, TAB_FOLDER_PICTURE))
db.commit()


# scan files
files = []
file_count = 0
find_files(dirs=[MP3_DIR], extensions=['.mp3'])

# result of file scan
print(F"Files: {file_count} scanned.")

db.commit()


db.close()
print('Exit!!!')
exit()
