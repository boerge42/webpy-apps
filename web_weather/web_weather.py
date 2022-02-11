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
from os import name
import web
import model
import datetime
import my_globals
from pathlib import Path
import re

from web.template import ALLOWED_AST_NODES
ALLOWED_AST_NODES.append('Constant')

# define url mappings
urls = (
        "/", "Index",
        "/diagrams/(.*)/", "Diagrams",
        "/heatmaps/(.*)/", "Heatmaps",
    )

# define Templates
render = web.template.render("templates", base="base", globals={"act_year":model.get_act_year, "days":my_globals.intervals, "convert_day":model.convert_day})

# ***************************************************************
class Index:

	# show page
    def GET(self):
        # current...
        current_sensor_values = dict()
        for key in my_globals.sensor_values:
            current_sensor_values[key] = model.current_sensor_point(key)
        # min/max...
        min_max_sensor_values=dict()
        # ...min/max today
        td_diff=datetime.datetime.now().time().hour*3600+datetime.datetime.now().time().minute*60+datetime.datetime.now().time().second
        td_diff=F"{td_diff}s"
        min_max_td=dict()
        for key in my_globals.sensor_values:
            min_max_td[key]=model.min_max(key, td_diff)
        min_max_sensor_values['td']=min_max_td
        # ...min/max over defined intervals
        for diff in my_globals.intervals:
            min_max_diff=dict()
            for key in my_globals.sensor_values:
                min_max_diff[key]=model.min_max(key, F'{diff}d')
            min_max_sensor_values[F'{diff}d']=min_max_diff
        return render.index(current_sensor_values, min_max_sensor_values)

# ***************************************************************
class Diagrams:

    # show page
    def GET(self, days):
        diagrams=[]
        for g in my_globals.graphs:
            d={}
            d['image']=F"{my_globals.csv_path}{g['value']}_{days}.png"
            diagrams.append(d)
        return render.diagrams(diagrams)

# ***************************************************************
class Heatmaps:

    # show page
    def GET(self, year):
        heatmap_diagrams=[]
        for h in my_globals.heatmaps:
            hm={}
            hm['image']=F"{my_globals.csv_path}heatmap_{h['value']}_{year}.png"
            heatmap_diagrams.append(hm)
        years=[]
        pathlist=Path(my_globals.csv_path).glob("heatmap_vbat_*.png")
        for path in pathlist:
            y=re.findall(r'\d+', path.name)
            try:
                years.append(y[0])
            except:
                pass
        return render.heatmaps(heatmap_diagrams, years)

# ***************************************************************
# ***************************************************************
# ***************************************************************
app = web.application(urls, globals())

if __name__ == "__main__":
    app.run()
