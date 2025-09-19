# *********************************************************************************************
#   web_manfreddb.py
# ------------------
#  Uwe Berger; 2025
#
#
#
#
# ---------
# Have fun!
#
# *********************************************************************************************

from os import name
import web
import model
import import_csv
import cgi


from web.template import ALLOWED_AST_NODES
ALLOWED_AST_NODES.append('Constant')


# define url mappings
urls = (
        "/", "Index",
        "/album_details/(.*)", "Album_details",
        '/login/', 'Login',
        '/logout/', 'Logout',
        '/upload/', 'Upload',
    )


web.config.debug = False

# define Templates
render = web.template.render("templates", base="base")

app = web.application(urls, globals())

session = web.session.Session(app, web.session.DiskStore('sessions'))

allowed = (
    ('x','y'),
)

upload_path = "upload"

# Maximum input we will accept when REQUEST_METHOD is POST
# 0 ==> unlimited input
# ~ cgi.maxlen = 10 * 1024 * 1024 # 10MB
cgi.maxlen = 5 * 1024 * 1024 # 5MB


# ***************************************************************
class Login:

    form = web.form.Form( web.form.Textbox('username', description="user: ", value=''),
        web.form.Password('password', description="password: ", value=''),
        web.form.Button('Login'),
    )
    
    # ****************************
    def GET(self):
        self.form['username'].value = ""
        self.form['password'].value = ""
        return render.login(self.form)

    # ****************************
    def POST(self):
        if not self.form.validates():
            return render.login(self.login_form)

        username = self.form['username'].value
        password = self.form['password'].value
        if (username,password) in allowed:
            session.logged_in = True
            raise web.seeother('/')
        else:
            self.form['username'].value = ""
            self.form['password'].value = ""
            return render.login(self.form)

# ***************************************************************
class Logout:
    
    # ****************************
    def GET(self):
        session.logged_in = False
        raise web.seeother('/login/')

# ***************************************************************
class Index:

    # define form
    form = web.form.Form(
        web.form.Textbox("search_txt", description="search text: "),
        web.form.Checkbox("limit", description="limit: ", value="bla", checked=True),
        web.form.Button("Search")
    )

	# ****************************
    def GET(self):
        if session.get('logged_in', False):
            records = []
            after_search = False
            form = self.form()
            return render.index(records, after_search, form)
        else:
            raise web.seeother('/login/')

    # ****************************
    def POST(self):
        form = self.form()
        if not form.validates():
            records = model.get_records("", form.d.limit)
        else:
            records = model.get_records(form.d.search_txt, form.d.limit)
        after_search = True
        return render.index(records, after_search, form)

# ***************************************************************
class Album_details:

  	# ****************************
    def GET(self, CDNr):
        if session.get('logged_in', False):
            print(CDNr)
            record = model.get_record_details(CDNr)
            titles = model.get_record_titles(CDNr)
            return render.album_details(record, titles)
        else:
            raise web.seeother('/login/')

# ***************************************************************
class Upload:

    form = web.form.Form(
        web.form.File('myfile', description="csv-file: "),
        web.form.Button('upload', type='submit')
    )

    # ****************************
    def GET(self):
        if session.get('logged_in', False):
            return render.upload(self.form, "")
        else:
            raise web.seeother('/login/')

    # ****************************
    def POST(self):
        msg = []
        try:
            x = web.input(myfile={})
            if 'myfile' in x and hasattr(x['myfile'], 'filename'):
                filename = x['myfile'].filename
                msg.append(f"[Info] Datei {filename} erfolgreich empfangen.")
                csv_filename = upload_path +'/'+ filename
                fout = open(csv_filename,'wb')
                fout.write(x.myfile.file.read())
                fout.close()
                msg.append(f"[Info] Datei {filename} kopiert.")

                ok, msg = import_csv.check_csv(csv_filename, msg)
                if ok != True:
                    msg.append(f"[Error] Import wegen Fehler in check_csv() abgebrochen!")
                else:
                    ok, msg = import_csv.import_csv(csv_filename, msg)
                    if  ok == False:
                        msg.append(f"[Error] Import wegen Fehler in import_csv() abgebrochen!")
                        exit()
                    else:
                        pass
            else:
                msg.append(f"[Error] Fehler beim Datei-Upload!")
        except ValueError:
            msg.append(f"[Error] Upload-Datei zu groß!")
        return render.upload(self.form, msg)


# ***************************************************************
# ***************************************************************
# ***************************************************************

if __name__ == "__main__":
    app.run()
