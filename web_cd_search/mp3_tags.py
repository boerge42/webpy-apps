#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# *********************************************************************************************
#    mp3_tags.py
# ------------------
#  Uwe Berger; 2021
#
# ...analize/convert mp3-tags...
#
# see also for scan mp3-tags:
#   https://stackoverflow.com/questions/24841191/get-mp3-play-time-using-eye3d-with-python
#
# ---------
# Have fun!
#
# *********************************************************************************************
import time

#import eyed3
from eyed3 import id3
from eyed3 import load

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


