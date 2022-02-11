# *********************************************************************************************
#     my_sql.py
# ------------------
#  Uwe Berger; 2021
#
# ...includes for sqlite3-DB as backend...
#
# ---------
# Have fun!
#
# *********************************************************************************************

import sqlite3

db_file = 'mp3_collection.db'

# Tabelle stations
tab_mp3_collection = 'mp3_collection'
mp3_collection_struct = [
        {'col_name':'artist',         'col_type':'text',       'col_key':''},   
        {'col_name':'album',          'col_type':'text',       'col_key':''},   
        {'col_name':'album_artist',   'col_type':'text',       'col_key':''},   
        {'col_name':'genre',          'col_type':'text',       'col_key':''},   
        {'col_name':'title',          'col_type':'text',       'col_key':''},   
        {'col_name':'year',           'col_type':'integer',    'col_key':''},   
        {'col_name':'track_nr',       'col_type':'integer',    'col_key':''},   
        {'col_name':'cd_id',          'col_type':'integer',    'col_key':''},   
        {'col_name':'sample_freq',    'col_type':'integer',    'col_key':''},   
        {'col_name':'bit_rate',       'col_type':'text',       'col_key':''},   
        {'col_name':'mode',           'col_type':'text',       'col_key':''},   
        {'col_name':'duration',       'col_type':'real',       'col_key':''},   
        {'col_name':'duration_str',   'col_type':'text',       'col_key':''},   
        {'col_name':'file_name',      'col_type':'text',       'col_key':'primary key'},   
        {'col_name':'file_size',      'col_type':'integer',    'col_key':''},   
        {'col_name':'file_modify',    'col_type':'text',       'col_key':''},   
        {'col_name':'parser_error',   'col_type':'text',       'col_key':''}
    ]


# ******************************************************************
def convert_str(s):
  s=s.replace("'","''")
  #s=s.replace('\x00','')
  return s


# ******************************************************************
def get_create_sql(struct, tab_name):
    s = f'create table if not exists {tab_name} ('
    comma = ''
    for l in struct:
        s=s+f"{comma} {l['col_name']} {l['col_type']} {l['col_key']}"
        comma = ','
    s = s +')'
    return s

# ******************************************************************
def get_insert_sql(struct, values, tab_name):
    s = f'insert or replace into {tab_name} values('
    comma = ''
    for l in struct:
        val = values[l['col_name']]
        if isinstance(val, str) == True:
            apos = "'"
            val = convert_str(val)
        else:
            apos = ""
        s=s+f"{comma} {apos}{val}{apos}"
        comma = ','
    s = s +')'
    return s

# ******************************************************************
def sql_execute(sql):
    db=sqlite3.connect(db_file)
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    result = cursor.execute(sql)
    l = []
    for row in result:
        l.append(row)
    db.commit()
    db.close()
    return l