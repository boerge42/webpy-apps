#
#
# mysql> describe mp3_collection;
# +--------------+--------------+------+-----+---------+-------+
# | Field        | Type         | Null | Key | Default | Extra |
# +--------------+--------------+------+-----+---------+-------+
# | artist       | varchar(255) | YES  |     | NULL    |       |
# | album        | varchar(255) | YES  |     | NULL    |       |
# | album_artist | varchar(255) | YES  |     | NULL    |       |
# | genre        | varchar(255) | YES  |     | NULL    |       |
# | title        | varchar(255) | YES  |     | NULL    |       |
# | year         | smallint(6)  | YES  |     | NULL    |       |
# | track_nr     | smallint(6)  | YES  |     | NULL    |       |
# | cd_id        | smallint(6)  | YES  |     | NULL    |       |
# | sample_freq  | int(11)      | YES  |     | NULL    |       |
# | bit_rate     | varchar(255) | YES  |     | NULL    |       |
# | mode         | varchar(255) | YES  |     | NULL    |       |
# | duration     | float        | YES  |     | NULL    |       |
# | duration_str | varchar(255) | YES  |     | NULL    |       |
# | file_name    | varchar(512) | NO   | PRI | NULL    |       |
# | file_size    | int(11)      | YES  |     | NULL    |       |
# | file_modify  | varchar(255) | YES  |     | NULL    |       |
# | parser_error | varchar(255) | YES  |     | NULL    |       |
# +--------------+--------------+------+-----+---------+-------+
#
#
# sqlite> .sch
# CREATE TABLE mp3_collection ( artist text , 
#                               album text, 
#                               album_artist text, 
#                               genre text, 
#                               title text, 
#                               year integer, 
#                               track_nr integer, 
#                               cd_id integer, 
#                               sample_freq integer, 
#                               bit_rate text, 
#                               mode text, 
#                               duration real, 
#                               duration_str text, 
#                               file_name text primary key, 
#                               file_size integer, 
#                               file_modify text, 
#                               parser_error text );
#
#
#