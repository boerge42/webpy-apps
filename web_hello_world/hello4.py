import web

urls = (
    '/(.*)', 'index'
)

render = web.template.render('templates/', base="base")

class index:
    def GET(self, hello):
        return render.index(hello)

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
