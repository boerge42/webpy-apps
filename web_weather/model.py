# ************************************************************************************************************
# 
# 
# ----------------
# Uwe Berger, 2021
#
# ---------
# Have fun!
#
# ************************************************************************************************************
from datetime import datetime
from influxdb import InfluxDBClient
import my_globals

influxdb=InfluxDBClient(host='nanotuxedo', port=8086, username='xxxx', password='yyyy', database='new_weatherstation')

#date_time_frm='%Y-%m-%d %H:%M:%S'
date_time_frm='%d.%m.%Y %H:%M:%S'

# *************************************************************************************************
def convert_day(d):
    return F"{d}d"

# *************************************************************************************************
def get_act_year():
    currentDateTime = datetime.now()
    date = currentDateTime.date()
    return date.strftime("%Y")

# *************************************************************************************************
def unixtime2frmstr(u):
    i=0
    while i < len(u):
        u[i]['time']=datetime.fromtimestamp(u[i]['time']).strftime(date_time_frm)
        i=i+1
    return u

# *************************************************************************************************
def current_sensor_point(sensor):
    ret=list(influxdb.query(F"select * from {sensor} order by desc limit 1", epoch='s').get_points())
    ret=unixtime2frmstr(ret)
    return ret

# *************************************************************************************************
def min_max(sensor, timediff):
    comma = ' '
    query = "select"
    for v in my_globals.sensor_values[sensor]:
        query = F"{query}{comma}min({v}) as min_{v}, max({v}) as max_{v}"
        comma=', '
    query = F"{query} from {sensor} where time > now() - {timediff}"
    ret=list(influxdb.query(query, epoch='s').get_points())
    return ret

# *************************************************************************************************
def get_csv_data_diagram(value, measurement, day_diff):
    ret=list(influxdb.query(F"select mean({value}) as {value} from {measurement} where time > now() - {day_diff}d group by time(5m) fill(linear)", epoch='s').get_points())
    return ret

# *************************************************************************************************
def get_csv_data_heatmap(value, sensor, year_start, year_end, fill):
    ret=list(influxdb.query(F"select mean({value}) as {value} from {sensor} where time >= {year_start} and time <= {year_end} group by time(5m) fill({fill})", epoch='s').get_points())
    return ret
