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

#db = web.database(dbn="sqlite", db="../db/mp3_collection.db")
db = web.database(dbn="mysql", host="host", db="mp3_collection", user="xxxx", pw="yyyy")

def get_artists(artist, limit):
    if limit==True:
        limit="limit 100"
    else:
        limit=""
    sql=f"select artist, album from mp3_collection where artist like \"%{artist}%\" group by artist, album order by artist {limit}"
    return list(db.query(sql))

def get_albums(album, limit):
    if limit==True:
        limit="limit 100"
    else:
        limit=""
    sql=f"select distinct album, album_artist, artist from mp3_collection where album like \"%{album}%\" order by album, album_artist, artist {limit}"
    return list(db.query(sql))

def get_titles(title, limit):
    if limit==True:
        limit="limit 100"
    else:
        limit=""
    sql=f"select distinct title, album, album_artist, artist from mp3_collection where title like \"%{title}%\" order by title, album, album_artist, artist {limit}"
    return list(db.query(sql))

def get_album_details(album):
#    sql = f"select artist, album, title, year, duration_str from mp3_collection where album = \"{album}\" order by artist, track_nr"
#    return list(db.query(sql))
	return list(db.select('mp3_collection', what='artist, album, title, year, duration_str', where={'album':album}, order='artist, track_nr'))
