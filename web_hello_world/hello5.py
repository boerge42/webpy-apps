import web

urls = (
    '/form', 'form',
    '/(.*)', 'index',
    )

render = web.template.render('templates/', base="base")

class index:
    def GET(self, hello):
        return render.index(hello)  


class form:

    valid = web.form.regexp(r"^[0-9]+$", ' --> must be numeric!')

    formular = web.form.Form(
                   web.form.Textbox("hello", valid, description="input: "),
                   web.form.Button("send...")
                )
                
    def GET(self):
        return render.form(self.formular) 
        
    def POST(self):
        if not self.formular.validates():
            return render.form(self.formular)
        else:
            return render.index(self.formular.d.hello) 


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
