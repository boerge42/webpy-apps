# *********************************************************************************************
#     my_sql.py
# ------------------
#  Uwe Berger; 2021
#
# ...includes for mysql-DB as backend...
#
# ---------
# Have fun!
#
# *********************************************************************************************
# ...
#
# #mysql> describe mp3_collection;
#+--------------+--------------+------+-----+---------+-------+
#| Field        | Type         | Null | Key | Default | Extra |
#+--------------+--------------+------+-----+---------+-------+
#| artist       | varchar(255) | YES  |     | NULL    |       |
#| album        | varchar(255) | YES  |     | NULL    |       |
#| album_artist | varchar(255) | YES  |     | NULL    |       |
#| genre        | varchar(255) | YES  |     | NULL    |       |
#| title        | varchar(255) | YES  |     | NULL    |       |
#| year         | smallint(6)  | YES  |     | NULL    |       |
#| track_nr     | smallint(6)  | YES  |     | NULL    |       |
#| cd_id        | smallint(6)  | YES  |     | NULL    |       |
#| sample_freq  | int(11)      | YES  |     | NULL    |       |
#| bit_rate     | varchar(255) | YES  |     | NULL    |       |
#| mode         | varchar(255) | YES  |     | NULL    |       |
#| duration     | float        | YES  |     | NULL    |       |
#| duration_str | varchar(255) | YES  |     | NULL    |       |
#| file_name    | varchar(512) | NO   | PRI | NULL    |       |
#| file_size    | int(11)      | YES  |     | NULL    |       |
#| file_modify  | varchar(255) | YES  |     | NULL    |       |
#| parser_error | varchar(255) | YES  |     | NULL    |       |
#+--------------+--------------+------+-----+---------+-------+

# Tabelle stations
tab_mp3_collection = 'mp3_collection'
mp3_collection_struct = [
        {'col_name':'album',          'col_type':'varchar(255)'},   
        {'col_name':'artist',         'col_type':'varchar(255)'},   
        {'col_name':'album_artist',   'col_type':'varchar(255)'},   
        {'col_name':'genre',          'col_type':'varchar(255)'},   
        {'col_name':'title',          'col_type':'varchar(255)'},   
        {'col_name':'year',           'col_type':'smallint(6)' },   
        {'col_name':'track_nr',       'col_type':'smallint(6)' },   
        {'col_name':'cd_id',          'col_type':'smallint(6)' },   
        {'col_name':'sample_freq',    'col_type':'int(11)'     },   
        {'col_name':'bit_rate',       'col_type':'varchar(255)'},   
        {'col_name':'mode',           'col_type':'varchar(255)'},   
        {'col_name':'duration',       'col_type':'float'       },   
        {'col_name':'duration_str',   'col_type':'varchar(255)'},   
        {'col_name':'file_name',      'col_type':'varchar(255)'},   
        {'col_name':'file_size',      'col_type':'int(11)'     },   
        {'col_name':'file_modify',    'col_type':'varchar(255)'},   
        {'col_name':'parser_error',   'col_type':'varchar(255)'}
    ]

# ...make it better!!!
mp3_collection_primary_key = ', primary key (file_name)'

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
        s=s+f"{comma} {l['col_name']} {l['col_type']}"
        comma = ','
    # ...make it better!!!
    s = s + mp3_collection_primary_key
    s = s +')'
    return s

# ******************************************************************
def get_insert_sql(struct, values, tab_name):
    s = f'replace into {tab_name} values('
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
