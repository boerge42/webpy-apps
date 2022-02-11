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

# sensors
sensor_values = {
    'TMP36': ['temperature'],
    'SHT15': ['temperature', 'humidity'],
    'BME280':['temperature', 'humidity', 'pressure_rel'],
    'BH1750':['luminosity'],
    'ESP':   ['vbat', 'awake_time']
}



# diagrams
graphs = [
    {'value':'temperature',     'sensors':['TMP36', 'SHT15', 'BME280']},
    {'value':'humidity',        'sensors':['SHT15', 'BME280']},
    {'value':'pressure_rel',    'sensors':['BME280']},
    {'value':'luminosity',      'sensors':['BH1750']},
    {'value':'vbat',            'sensors':['ESP']},
    {'value':'awake_time',      'sensors':['ESP']}
]

# ...in days
intervals = ['1', '7', '30', '120']

# heatmaps (over a year)
heatmaps = [
    {'value':'temperature',  'sensor':'TMP36',  'fill': '101'},
    {'value':'humidity',     'sensor':'SHT15',  'fill': '101'},
    {'value':'pressure_rel', 'sensor':'BME280', 'fill': '1100'},
    {'value':'luminosity',   'sensor':'BH1750', 'fill': '0'},
    {'value':'vbat',         'sensor':'ESP',    'fill': '5'},
    {'value':'awake_time',   'sensor':'ESP',    'fill': '61000'}
]

# output-path
csv_path='static/'
