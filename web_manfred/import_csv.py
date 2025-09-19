#
# CSV-Datei (Feldbezeichnungen):

# idx field(csv)        table           field(sql)
# 0   "CDNr",           album, title    CDNr
# 1   "Genre",          album           Genre
# 2   "Interpret",      album           Interpret
# 3   "Album",          album           Album
# 4   "Dauer",          album           Dauer
# 5   "Tracks",         album           Tracks
# 6   "Herausgeber",    album           Herausgeber
# 7   "Jahr",           album           Jahr
# 8   "Lagerort",       album           Lagerort
# 9   "Lagerplatz",     album           Lagerplatz
# 10  "Wertung",        album           Wertung
# 11  "Anmerkungen",    album           Anmerkungen
# 12  "Manfred",        album           Manfred
# 13  "Track",          title           Track
# 14  "Länge",          title           Länge
# 15  "Titel",          title           Titel
# 16  "Interpret",      title           Interpret
# 17  "Hinweis"         title           Hinweis
#
#
# CSV-Codierung: ISO-8859-1 --> latin1
#
#
#
# select * from album a, title t where a.cdnr = t.cdnr and a.cdnr = "217"
#
#
#
#
#
import csv
import sqlite3

db_filename = "manfred.db"
csv_filename = "archiv_test_01_Sep_2025.csv"

tab_album = "album"
tab_title = "title"

# Mappings (csv -> sql) und sql-table-definitions
# (ein constraint kann auch "default ..." sein

mapping_album = [
    {"field":"CDNr",        "csv_idx":0,    "type":"text",    "constraint":"primary key",   "value_border":'\"'},
    {"field":"Genre",       "csv_idx":1,    "type":"text",    "constraint":"",              "value_border":'\"'},
    {"field":"Interpret",   "csv_idx":2,    "type":"text",    "constraint":"",              "value_border":'\"'},
    {"field":"Album",       "csv_idx":3,    "type":"text",    "constraint":"",              "value_border":'\"'},
    {"field":"Dauer",       "csv_idx":4,    "type":"text",    "constraint":"",              "value_border":'\"'},
    {"field":"Tracks",      "csv_idx":5,    "type":"text",    "constraint":"",              "value_border":'\"'},
    {"field":"Herausgeber", "csv_idx":6,    "type":"text",    "constraint":"",              "value_border":'\"'},
    {"field":"Jahr",        "csv_idx":7,    "type":"text",    "constraint":"",              "value_border":'\"'},
    {"field":"Lagerort",    "csv_idx":8,    "type":"text",    "constraint":"",              "value_border":'\"'},
    {"field":"Lagerplatz",  "csv_idx":9,    "type":"text",    "constraint":"",              "value_border":'\"'},
    {"field":"Wertung",     "csv_idx":10,   "type":"text",    "constraint":"",              "value_border":'\"'},
    {"field":"Anmerkungen", "csv_idx":11,   "type":"text",    "constraint":"",              "value_border":'\"'},
    {"field":"Manfred",     "csv_idx":12,   "type":"text",    "constraint":"",              "value_border":'\"'},
]

mapping_title = [
    {"field":"CDNr",        "csv_idx":0,    "type":"text",    "constraint":"",              "value_border":'\"'},
    {"field":"Track",       "csv_idx":13,   "type":"text",    "constraint":"",              "value_border":'\"'},
    {"field":"Länge",       "csv_idx":14,   "type":"text",    "constraint":"",              "value_border":'\"'},
    {"field":"Titel",       "csv_idx":15,   "type":"text",    "constraint":"",              "value_border":'\"'},
    {"field":"Interpret",   "csv_idx":16,   "type":"text",    "constraint":"",              "value_border":'\"'},
    {"field":"Hinweis",     "csv_idx":17,   "type":"text",    "constraint":"",              "value_border":'\"'},
]

table_index = [
    {"table":f"{tab_title}",     "idx_name":"idx_title",   "idx_fields":"CDnr"},
]


# *******************************************************************************
def check_csv(fn, msg):

    # *********************************
    # es darf nicht 2x den gleichen Index in den Mappings geben!
    def check_new_entry(csv_col, idx):
        for c in csv_col:
            if c["idx"] == idx:
                return False
        return True


    # *********************************
    # *********************************
    
    # aus Mappings (album/title) eine Gesamtliste alle Spaltennamen generieren
    csv_mapping = []
    for m in mapping_album:
        if check_new_entry(csv_mapping, m["csv_idx"]):
            col = {}
            col["idx"] = m["csv_idx"]
            col["field"] = m["field"]
            csv_mapping.append(col)
    for m in mapping_title:
        if check_new_entry(csv_mapping, m["csv_idx"]):
            col = {}
            col["idx"] = m["csv_idx"]
            col["field"] = m["field"]
            csv_mapping.append(col)
        
    # Datei als csv oeffnen und Header ueberpruefen
    try:
        with open(fn, 'r', newline='', encoding='latin1') as csvfile:
            csv_reader_object = csv.reader(csvfile, delimiter=",")
            # in der ersten Zeile in der csv-Datei stehen die Spaltennamen 
            csv_columns = next(csv_reader_object)
            # Anzahl Spalten von csv und Mappingdefinition muss uebereinstimmen
            if len(csv_columns) != len(csv_mapping):
                msg.append("[Error] check_csv(): Spaltenanzahl passt nicht zur Mappingdefinition!")
                return False, msg
            # Indizes/Spaltenname von csv und Mappingdefinition muessen uebereinstimmen
            for m in csv_mapping:
                if csv_columns[m["idx"]] != m["field"]:
                    msg.append(f'[Error] check_csv(): CSV-Spaltenname ({csv_columns[m["idx"]]}) passt nicht zur Mappingdefinition ({m["idx"]}, {m["field"]})!')
                    return False, msg
    except FileNotFoundError:
            msg.append(f'[Error] check_csv(): Datei nicht vorhanden ({fn})!')
            return False, msg
    except csv.Error as e:
            msg.append(f'[Error] check_csv(): CSV-Error file {fn}, line {csv_reader_object.line_num}: {e}')
            return False, msg
        
    # wenn bis hier gekommen, passt alles!
    msg.append("[Info] check_csv(): Test bestanden.")
    return True, msg


# *******************************************************************************
def import_csv(fn, msg):

    # *******************************************************************************
    def str_quote(txt):
        # ~ print(txt)
        # ~ txt = txt.replace("'", "''")
        txt = txt.replace('"', '')
        # ~ print(txt)
        return txt

    try:
        db_conn = sqlite3.connect(db_filename)
        db = db_conn.cursor()

        # create table album
        sql = f"create table if not exists {tab_album} ("
        comma = ""
        for c in mapping_album:
            sql = f'{sql}{comma}{c["field"]} {c["type"]} {c["constraint"]}'
            comma=", "
        sql = f'{sql}) without rowid'
        db.execute(sql)
        # ~ print(sql)
        # ~ print("")

        # create table title
        sql = f"create table if not exists {tab_title} ("
        comma = ""
        for c in mapping_title:
            sql = f'{sql}{comma}{c["field"]} {c["type"]} {c["constraint"]}'
            comma=", "
        sql = f'{sql})'
        db.execute(sql)
        # ~ print(sql)
        # ~ print("")

        # create index on tables
        for i in table_index:
            sql = f'create index if not exists {i["idx_name"]} on {i["table"]} ({i["idx_fields"]})'
            db.execute(sql)
            # ~ print(sql)
            
        # album, title leeren
        sql = f"delete from {tab_title}"
        db.execute(sql)
        sql = f"delete from {tab_album}"
        db.execute(sql)

        # csv auslesen
        with open(fn, 'r', newline='', encoding='latin1') as csvfile:
            csv_reader_object = csv.reader(csvfile, delimiter=",")
            
            colnr = 0
            cdnr_prev = ""
            for row in csv_reader_object:
                if colnr > 0:
                    
                    # table album
                    # insert into title value (..., ...) --> value-Reihenfolge ist durch create festgelegt!
                    if cdnr_prev != row[0]:
                        cdnr_prev = row[0]
                        sql = f"insert into {tab_album} values ("
                        comma = ""
                        for c in mapping_album:
                            sql = f'{sql}{comma}{c["value_border"]}{str_quote(row[c["csv_idx"]])}{c["value_border"]}'
                            comma=", "
                        sql = f'{sql})'
                        db.execute(sql)
                                
                    # table title
                    # insert into title values (..., ...) --> value-Reihenfolge ist durch create festgelegt!
                    sql = f"insert into {tab_title} values ("
                    comma = ""
                    for c in mapping_title:
                        sql = f'{sql}{comma}{c["value_border"]}{str_quote(row[c["csv_idx"]])}{c["value_border"]}'
                        comma=", "
                    sql = f'{sql})'
                    db.execute(sql)

                colnr += 1

            msg.append(f'[Info] import_csv(): {colnr-1} Zeilen importiert.')

        db_conn.commit()
        db_conn.close()
        return True, msg
    except Exception as e:
        msg.append(f'[Error] import_csv(): in file {fn}, csv line {csv_reader_object.line_num} -> {e}!')
        db_conn.rollback()
        db_conn.close()
        return False, msg
