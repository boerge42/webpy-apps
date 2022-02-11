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
import web
from web import form
import model

from web.template import ALLOWED_AST_NODES
ALLOWED_AST_NODES.append('Constant')

# define url mappings
urls = (
        "/", "Index",
        "/lights", "Index",
        "/sensors", "Sensors",
        "/details/(.*)/(.*)", "Details",
        "/set_state/(.*)/(.*)/(.*)", "Set_state",
    )

# define details_form
details_form = form.Form()

# define Templates
render = web.template.render("templates", base="base")

# ***************************************************************
class Index:

    def GET(self):
        tab_lights = model.get_tab_lights()
        return render.index(tab_lights)

# ***************************************************************
class Sensors:

    def GET(self):
        tab_sensors = model.get_tab_sensors()
        return render.sensors(tab_sensors)

# ***************************************************************
class Details:
    
    def GET(self, type, id):
        global details_form
        text=model.get_id_text(type, id)
        args=model.get_id_form_args(type, id)
        details_form = form.Form(*args)
        return render.details(text, type, id, details_form)

    def POST(self, type, id):
        global details_form
        if details_form.validates():
            if type == "lights":
                print(model.set_light_all_states(id, details_form.d))
            elif type == "sensors":
                print(model.set_sensor_all_config(id, details_form.d))
            else:
                pass
        else:
            print("ERROR VALIDATION FORM!!!")
            text=model.get_id_text(type, id)
            return render.details(text, type, id, details_form)
        text=model.get_id_text(type, id)
        args=model.get_id_form_args(type, id)
        details_form = form.Form(*args)
        return render.details(text, type, id, details_form)

# ***************************************************************
class Set_state:

    def GET(self, state, value, id):
        print(model.set_light_state(id, state, value))
        tab_lights = model.get_tab_lights()
        return render.index(tab_lights)

# ***************************************************************
# ***************************************************************
# ***************************************************************
app = web.application(urls, globals())

if __name__ == "__main__":
    app.run()
