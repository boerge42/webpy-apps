

import model
from datetime import datetime, tzinfo
from dateutil import tz
import pytz

# datetime convert :-)
dt_str      = "2021-12-15T10:03Z"
format  = "%Y-%m-%dT%H:%MZ"

dt_utc = datetime.strptime(dt_str, "%Y-%m-%dT%H:%MZ")
dt_utc = dt_utc.replace(tzinfo=pytz.UTC)
print('Datetime in UTC Time zone: ', dt_utc)

local_zone = tz.tzlocal()
dt_local = dt_utc.astimezone(local_zone)
print('Datetime in Local Time zone: ', dt_local)

local_time_str = dt_local.strftime("%d.%m.%Y %H:%M")
print('Time as string in Local Time zone: ', local_time_str)

# test all lights
#tab_lights = model.get_tab_lights()
#for l in tab_lights:
#    print(
#           l["id"],  "|",
#           l["name"],"|",
#           #l["manufacturername"],"|",
#           #l["modelid"],"|",
#           l["type"],"|",
#           l["reachable"],"|",
#           l["lastseen"],"|",
#           l["on"],"|",
#           l["bri"],"|",
#         )
#print("*******")


# test all lights
#tab_sensors = model.get_tab_sensors()
#for l in tab_sensors:
#    print(
#           l["id"],  "|",
#           l["name"],"|",
#           #l["manufacturername"],"|",
#           #l["modelid"],"|",
#           l["type"],"|",
#           l["reachable"],"|",
#           l["lastseen"],"|",
#           l["battery"],"|",
#           l["value"],"|",
#           l["unit"],"|",
#         )
#print("*******")

# test set_light_state
#print(model.set_light_state(2, "on", "true"))

#print(model.get_id_text("lights", 2))
#print("*****")
#data= {'bri': 255, 'on': 'true', 'submit': None}
#print(model.set_light_all_states(2, data))
#print("*****")
#print(model.get_id_text("lights", 2))
#print("*****")


# test get_id_state
#print(model.get_id_state("lights", 2))

#print(model.get_id_text("lights", 5))
#print("*******")
#print(model.get_id_text("sensors", 20))
