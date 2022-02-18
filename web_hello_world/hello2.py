import web

from web.template import ALLOWED_AST_NODES
ALLOWED_AST_NODES.append('Constant')


urls = (
    '/', 'index'
)

render = web.template.render('templates/')

class index:
    def GET(self):
        hello = 'Hello world!'
        return render.index(hello)

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
