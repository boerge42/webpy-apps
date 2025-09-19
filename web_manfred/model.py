# *********************************************************************************************
#
#      model.py
# ---------------------
#   Uwe Berger; 2025
#
# ...access to database...
#
# ---------
# Have fun!
#
# *********************************************************************************************

import web

db = web.database(dbn="sqlite", db="manfred.db")

# ***********************************************************************
def get_records(search_txt, limit):
    if limit==True:
        limit="limit 100"
    else:
        limit=""
    sql=f"select interpret, album, cdnr from album where interpret like \"%{search_txt}%\" or album like \"%{search_txt}%\" order by interpret, Album {limit}"
    return list(db.query(sql))
    
# ***********************************************************************
def get_record_details(CDNr):
    return list(db.select("album", what='*', where={'CDNr':CDNr}))

# ***********************************************************************
def get_record_titles(CDNr):
    return list(db.select("title", what='*', where={'CDNr':CDNr}))

