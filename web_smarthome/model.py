# **********************************************************************
# 
# 
# ----------------
# Uwe Berger, 2021
#
# ---------
# Have fun!
#
#
# **********************************************************************

#from os import stat
from os import stat
import requests
from web import form
from datetime import datetime, tzinfo
from dateutil import tz
import pytz

api_key = "apikeyxyzbla"
server  = "http://deconzhost:80"

state_form = [
        {"state":"alert",           "type":"dropdown", "args":['"none"', '"select"', '"lselect"']},
        {"state":"bri",             "type":"textbox",                                               "validator" : r"^([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])$", "validator_txt" : " --> must be numeric and between 0...255!"},
        {"state":"colorloopspeed",  "type":"textbox",                                               "validator" : r"^([01]?[1-9]?[0-9]|2[0-4][0-9]|25[0-5])$", "validator_txt" : " --> must be numeric and between 1???...255! (colorloopspeed)!"},
        {"state":"ct",              "type":"textbox",                                               "validator" : r"^[0-9]+$", "validator_txt" : " --> must be numeric (ct)!"},
        {"state":"effect",          "type":"dropdown", "args":["none", "colorloop"]},
        {"state":"hue",             "type":"textbox",                                               "validator" : r"^[0-9]+$", "validator_txt" : " --> must be numeric (hue)!"},
        {"state":"on",              "type":"dropdown", "args":["true", "false"]},
        {"state":"sat",             "type":"textbox",                                               "validator" : r"^([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])$", "validator_txt" : " --> must be numeric and between 0...255!"},
        {"state":"transitiontime",  "type":"textbox",                                               "validator" : r"^[0-9]+$", "validator_txt" : " --> must be numeric!"},
        {"state":"xy",              "type":"textbox",                                               "validator" : r"",         "validator_txt": " xy --> ???!"},
    ]

config_form = [
        {"sensor_type":"ZHAPresence", "config":"delay",     "type":"textbox",                       "validator" : r"^[0-9]+$", "validator_txt" : " --> must be numeric and >=0!"},
        {"sensor_type":"ZHAPresence", "config":"duration",  "type":"textbox",                       "validator" : r"^[0-9]+$", "validator_txt" : " --> must be numeric and >=0!"},
    ]

# **********************************************************************
def convert_utc_local(dt_str):
    dt_utc = datetime.strptime(dt_str, "%Y-%m-%dT%H:%MZ")
    dt_utc = dt_utc.replace(tzinfo=pytz.UTC)
    local_zone = tz.tzlocal()
    dt_local = dt_utc.astimezone(local_zone)
    local_time_str = dt_local.strftime("%d.%m.%Y %H:%M")
    return local_time_str

# **********************************************************************
def get_tab_lights():
    response = requests.get(F"{server}/api/{api_key}/lights")
    lights=response.json()
    tab_lights = []
    for key in lights:
        line={}
        line["id"]   = key
        line["id_str"] = "%03d" % (int(key),)
        line["name"] = lights[key]["name"]
        line["manufacturername"] = lights[key]["manufacturername"]
        line["modelid"] = lights[key]["modelid"]
        line["type"] = lights[key]["type"]
        line["reachable"] = lights[key]["state"]["reachable"]
        # icon for reachable...
        line["reachable_icon"] = F'static/{lights[key]["state"]["reachable"]}.png'
        line["lastseen"] = convert_utc_local(lights[key]["lastseen"])
        try:
            line["on"] = lights[key]["state"]["on"]
            if line["on"] == True:
                line["on_link"]= "false"
            else:
                line["on_link"]= "true"
            # icon for on_link...
            line["on_link_icon"] = F'static/light-{lights[key]["state"]["on"]}.png'
        except:
            line["on"] = ""
            line["on_link"] = ""
            line["on_link_icon"] = ""
        try:
            line["bri"] = lights[key]["state"]["bri"]
        except:
            line["bri"] = ""
        tab_lights.append(line)
    return sorted(tab_lights, key=lambda x: x["id_str"])

# **********************************************************************
def get_tab_sensors():
    response = requests.get(F"{server}/api/{api_key}/sensors")
    sensors=response.json()
    tab_sensors = []
    for key in sensors:
        line={}
        line["id"] = key
        line["id_str"] = "%03d" % (int(key),)
        line["name"] = sensors[key]["name"]
        line["manufacturername"] = sensors[key]["manufacturername"]
        line["modelid"] = sensors[key]["modelid"]
        line["type"] = sensors[key]["type"]
        try:
            line["reachable"] = sensors[key]["config"]["reachable"]
            # icon for reachable...
            line["reachable_icon"] = F'static/{sensors[key]["config"]["reachable"]}.png'
        except:
            line["reachable"] = ""
            line["reachable_icon"] = ""
        try:
            line["lastseen"] = convert_utc_local(sensors[key]["lastseen"])
        except:
            line["lastseen"] = ""
        try:
            line["battery"] = sensors[key]["config"]["battery"]
        except:
            line["battery"] = ""
        line["value"] = ""
        line["unit"] = ""
        if line["type"] == "ZHATemperature":
            line["value"] = sensors[key]["state"]["temperature"]/100
            line["unit"] = "°C"
        elif line["type"] == "ZHAPressure":
            line["value"] = sensors[key]["state"]["pressure"]
            line["unit"] = "hPa"
        elif line["type"] == "ZHAHumidity":
            line["value"] = sensors[key]["state"]["humidity"]/100
            line["unit"] = "%"
        elif line["type"] == "ZHAPresence":
            line["value"] = sensors[key]["state"]["presence"]
            line["unit"] = "(presence)"
        elif line["type"] == "ZHASwitch":
            line["value"] = sensors[key]["state"]["buttonevent"]
            line["unit"] = "(buttonevent)"
        elif line["type"] == "ZHAFire":
            line["value"] = sensors[key]["state"]["fire"]
            line["unit"] = "(fire)"
        tab_sensors.append(line)
    return sorted(tab_sensors, key=lambda x: x["id_str"])

# **********************************************************************
def dict_walk(t, l, r):
    for k, v in t.items():
        spaces=" "*l
        if isinstance(v, dict):
            r = F"{r}{spaces}{k}:\n"
            r = dict_walk(v, l+len(k), r)
        else:
            r = F"{r}{spaces}{k}: {v}\n"
    return r
  
# **********************************************************************
def get_id_text(type, id):
    response = requests.get(F"{server}/api/{api_key}/{type}/{id}")
    data=response.json()    
    return (dict_walk(data, 0, ""))

# **********************************************************************
def get_id_state_form(type, id):
    response = requests.get(F"{server}/api/{api_key}/{type}/{id}")
    data=response.json()  
    args = ()
    button = False
    for state in state_form:
        if state["state"] in data["state"]:
            if state["type"] == "dropdown":
                args = args + (form.Dropdown(state["state"], description=state["state"], args=state["args"], value=str(data["state"][state["state"]]).lower()), )
            else:
                # textbox!
                validator = form.regexp(state["validator"], state["validator_txt"])
                args = args + (form.Textbox(state["state"], validator, description=state["state"], value=data["state"][state["state"]]), )
            button = True
    if button:
        args = args + (form.Button("submit", html="<b>Send</b>", type="submit", description="change"), )
    return args

# **********************************************************************
def get_id_config_form(type, id):
    response = requests.get(F"{server}/api/{api_key}/{type}/{id}")
    data=response.json()  
    args = ()
    button = False
    for config in config_form:
        if data["type"]==config["sensor_type"] and config["config"] in data["config"]:
            if config["type"] == "dropdown":
                args = args + (form.Dropdown(config["config"], description=config["config"], args=config["args"], value=str(data["config"][config["config"]]).lower()), )
            else:
                # textbox!
                validator = form.regexp(config["validator"], config["validator_txt"])
                args = args + (form.Textbox(config["config"], validator, description=config["config"], value=data["config"][config["config"]]), )
            button = True
    if button:
        args = args + (form.Button("submit", html="<b>Send</b>", type="submit", description="change"), )
    return args

# **********************************************************************
def get_id_form_args(type, id):
    if type == "lights":
        args=get_id_state_form(type, id)
    elif type == "sensors":
        args=get_id_config_form(type, id)
    else:
        args=()
    return args

# **********************************************************************
def set_light_state(id, state, value):
    response = requests.put(F"{server}/api/{api_key}/lights/{id}/state", data=F'{{ "{state}":{value} }}')
    return response.status_code, response.text

# **********************************************************************
def set_light_all_states(id, s):
    d="{"
    komma=""
    for name in s:
        if name != "submit":
            d=F'{d}{komma}"{name}":{s[name]} '
            komma=","
    d=F'{d}}}'
    print(d)
    response = requests.put(F"{server}/api/{api_key}/lights/{id}/state", data=d)
    return response.status_code, response.text

# **********************************************************************
def set_sensor_all_config(id, s):
    d="{"
    komma=""
    for name in s:
        if name != "submit":
            d=F'{d}{komma}"{name}":{s[name]} '
            komma=","
    d=F'{d}}}'
    print(d)
    response = requests.put(F"{server}/api/{api_key}/sensors/{id}/config", data=d)
    return response.status_code, response.text