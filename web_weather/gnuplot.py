# ************************************************************************************************************
# 
# (my!) gnuplot.py to generate my weather charts/heatmaps
# -------------------------------------------------------
#                 Uwe Berger, 2021
#
# ...see variables/parameters at the beginning :-)
#
# ---------
# Have fun!
#
# ************************************************************************************************************

from influxdb import InfluxDBClient
from datetime import datetime
import my_globals
import model
import os

# path to gnuplot
cmd_gnuplot = 'gnuplot'

# ...delete all csv...
cmd_delete_all_csv = F"rm {my_globals.csv_path}*.csv"


# *************************************************************************************************
def unixtime2frmstr(u):
    i=0
    while i < len(u):
        u[i]['time']=datetime.fromtimestamp(u[i]['time']).strftime(date_time_frm)
        i=i+1
    return u

# *************************************************************************************************
# *************************************************************************************************
# *************************************************************************************************

# data for diagrams...
date_time_frm='%d.%m.%Y %H:%M:%S'
for i in my_globals.intervals:
    for v in my_globals.graphs:
        for s in v['sensors']:
            ret=model.get_csv_data_diagram(v['value'], s, i)
            ret=unixtime2frmstr(ret)
            csv=open(F"{my_globals.csv_path}{v['value']}_{s}_{i}d.csv", "w")
            for r in ret:
                csv.write(F"{r['time']};{r[v['value']]}\n")
            csv.close()
    os.system(F"{cmd_gnuplot} -e \"days='{i}'\" -e \"path='{my_globals.csv_path}'\" graph_arg.gp")

# data for heatmaps..., for this year
year= datetime.today().strftime('%Y')
year_start=int(datetime(int(year), 1, 1, 0, 0, 0).strftime('%s'))*1000000000
year_end=int(datetime(int(year), 12, 31, 23, 59, 59).strftime('%s'))*1000000000
date_time_frm='%Y-%m-%d'
for h in my_globals.heatmaps:
    ret=model.get_csv_data_heatmap(h['value'], h['sensor'], year_start, year_end, h['fill'])
    ret=unixtime2frmstr(ret)
    diff = 0.0833 # eine Stunde in 5min-Teile 1/12
    d = 0
    csv=open(F"{my_globals.csv_path}heatmap_{h['value']}_{year}.csv", "w")
    for r in ret:
        csv.write(F"{r['time']}; {round(d,2)}; {r[h['value']]}\n")
        d = d+diff
        if d >= 23.99: d=0
    csv.close()
os.system(F"{cmd_gnuplot} -e \"year='{year}'\" -e \"path='{my_globals.csv_path}'\" heatmap_arg.gp")

# delete all .csv
os.system(cmd_delete_all_csv)