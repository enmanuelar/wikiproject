import main, wikidb, utils, logging
from json import JSONEncoder
from google.appengine.ext import db

class SignupHandler(main.Handler):
    def get(self):
        self.render("signup.html")

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        #verify = self.request.get("verify")
        email = self.request.get("email")
        validation = self.request.get("validation")
        if utils.get_userdb_cache(username) and validation == "true":
            response = JSONEncoder().encode({"status": True})
            self.response.out.write(response)
        else:
            response = JSONEncoder().encode({"status": False})
            self.response.out.write(response)
        if validation == "false":
            hash_pw = utils.hashpw(password, salt=None)
            if email:
                user = wikidb.Users(username=username, password=hash_pw[0], email=email, salt=hash_pw[1])
            else:
                user = wikidb.Users(username=username, password=hash_pw[0], salt=hash_pw[1])
            user_key = user.put()
            utils.add_userdb_cache(username, user_key)
            cookie = str(utils.hash_cookie(username))
            self.response.headers.add_header('Set-Cookie', 'name=%s; Path=/' % cookie)
            self.response.headers.add_header('Set-Cookie', 'user_id=%s; Path=/' % user_key.id())
            self.redirect("/")

app = main.webapp2.WSGIApplication([
    ('/signup', SignupHandler)
], debug=True)