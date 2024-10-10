# *********************************************************************************************
#
#      model.py
# ---------------------
#   Uwe Berger; 2021
#
# ...access to database...
#
# ---------
# Have fun!
#
# *********************************************************************************************

import web

TAB_MP3_COLLECTION = "test_mp3_collection"
TAB_FOLDER_PICTURE = "test_folder_picture"

db = web.database(dbn="mysql", host="dockerpi", db="mp3_collection", user="xxxx", pw="yyyy")

def get_artists(artist, limit):
    if limit==True:
        limit="limit 100"
    else:
        limit=""
    sql=f"select artist, album, b.present as present, a.path as path, convert(b.picture, char) as picture from {TAB_MP3_COLLECTION} a, {TAB_FOLDER_PICTURE} b where artist like \"%{artist}%\" and a.path = b.path group by artist, album order by artist {limit}"
    return list(db.query(sql))

def get_albums(album, limit):
    if limit==True:
        limit="limit 100"
    else:
        limit=""
    sql=f"select distinct album, artist, a.path as path, convert(b.picture, char) as picture from {TAB_MP3_COLLECTION} a, {TAB_FOLDER_PICTURE} b where album like \"%{album}%\" and a.path = b.path order by album, artist {limit}"
    return list(db.query(sql))

def get_titles(title, limit):
    if limit==True:
        limit="limit 100"
    else:
        limit=""
    sql=f"select distinct title, album, album_artist, artist, path from {TAB_MP3_COLLECTION} where title like \"%{title}%\" order by title, album, album_artist, artist {limit}"
    return list(db.query(sql))

def get_album_details(path):
    return list(db.select(TAB_MP3_COLLECTION, what='artist, album, title, year, duration_str', where={'path':path}, order='artist, track_nr'))

def get_album_cover(path):
    sql=f"select distinct convert(b.picture, char) as picture from {TAB_MP3_COLLECTION} a, {TAB_FOLDER_PICTURE} b where a.path =\"{path}\" and a.path = b.path"
    return list(db.query(sql))
