# *********************************************************************************************
#    cd_search.py
# ------------------
#  Uwe Berger; 2021
#
#
# https://stackoverflow.com/questions/9134553/web-py-todo-list-with-login
# https://webpy.org/docs/0.3/sessions
#
# login-Felder leeren???!!!
#
# ---------
# Have fun!
#
# *********************************************************************************************

from os import name
import web
import model

from web.template import ALLOWED_AST_NODES
ALLOWED_AST_NODES.append('Constant')


# define url mappings
urls = (
        "/", "Index",
        "/album_search/", "Album_search",
        "/title_search/", "Title_search",
        "/album_details/(.*)", "Album_details",
        '/login/', 'Login',
        '/logout/', 'Logout',
    )


web.config.debug = False

# define Templates
render = web.template.render("templates", base="base")

app = web.application(urls, globals())

session = web.session.Session(app, web.session.DiskStore('sessions'))

allowed = (
    ('xxxx','yyyy'),
)

# ***************************************************************
class Login:

    form = web.form.Form( web.form.Textbox('username', description="user: ", value=''),
        web.form.Password('password', description="password: ", value=''),
        web.form.Button('Login'),
        )

    def GET(self):
        f = self.form()
        return render.login(f)

    def POST(self):
        if not self.form.validates():
            return render.login(self.login_form)

        username = self.form['username'].value
        password = self.form['password'].value
        if (username,password) in allowed:
            session.logged_in = True
            raise web.seeother('/')
        else:
            return render.login(self.form)

# ***************************************************************
class Logout:
    def GET(self):
        session.logged_in = False
        raise web.seeother('/login/')

# ***************************************************************
class Index:

    # define form
    form = web.form.Form(
        web.form.Textbox("artist", description="artist: "),
        web.form.Checkbox("limit", description="limit: ", value="bla", checked=True),
        web.form.Button("Search")
    )

	# show page
    def GET(self):
        if session.get('logged_in', False):
            artists = []
            form = self.form()
            return render.index(artists, form)
        else:
            raise web.seeother('/login/')

    # filter artists
    def POST(self):
        form = self.form()
        if not form.validates():
            artists = model.get_artists("", form.d.limit)
        else:
            artists = model.get_artists(form.d.artist, form.d.limit)
        return render.index(artists, form)


# ***************************************************************
class Album_search:

    # define form
    form = web.form.Form(
        web.form.Textbox("album", description="album: "),
        web.form.Checkbox("limit", description="limit: ", value="bla", checked=True),
        web.form.Button("Search")
    )

    # show page
    def GET(self):
        if session.get('logged_in', False):
            form = self.form()
            albums=[]
            return render.album_search(albums, form)
        else:
            raise web.seeother('/login/')


    # filter albums
    def POST(self):
        form = self.form()
        if not form.validates():
            albums = model.get_albums("", form.d.limit)
        else:
            albums = model.get_albums(form.d.album, form.d.limit)
        return render.album_search(albums, form)


# ***************************************************************
class Title_search:

    # define form
    form = web.form.Form(
        web.form.Textbox("title", description="title: "),
        web.form.Checkbox("limit", description="limit: ", value="bla", checked=True),
        web.form.Button("Search")
    )

  	# show page
    def GET(self):
        if session.get('logged_in', False):
            form = self.form()
            titles = []
            return render.title_search(titles, form)
        else:
            raise web.seeother('/login/')


    # filter titles
    def POST(self):
        form = self.form()
        if not form.validates():
            titles = model.get_titles("", form.d.limit)
        else:
            titles = model.get_titles(form.d.title, form.d.limit)
        return render.title_search(titles, form)

# ***************************************************************
class Album_details:

  	# show page
    def GET(self, album):
        if session.get('logged_in', False):
            print(album)
            albums = model.get_album_details(album)
            return render.album_details(albums)
        else:
            raise web.seeother('/login/')


# ***************************************************************
# ***************************************************************
# ***************************************************************

if __name__ == "__main__":
    app.run()
