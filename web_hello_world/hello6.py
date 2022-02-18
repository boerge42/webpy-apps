import web

from web.template import ALLOWED_AST_NODES
ALLOWED_AST_NODES.append('Constant')


urls = (
    '/', 'database'
)

db = web.database(dbn='sqlite', db='db.sqlite')

render = web.template.render('templates/', base="base")

class database:
    def GET(self):
        fn = db.select("person") 
        return render.database(fn)

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
