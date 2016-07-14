import main, wikidb, utils, logging
from json import JSONEncoder
from google.appengine.ext import db

class SignupHandler(main.Handler):
    def get(self):
        self.render("signup.html")

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")
        validation = self.request.get("validation")
        logging.error(username)
        if db.Query(wikidb.Users).filter('username =', username).get():
            response = JSONEncoder().encode({"status": True})
            self.response.out.write(response)
        else:
            response = JSONEncoder().encode({"status": False})
            self.response.out.write(response)
        if validation:
            user = wikidb.Users(username = username, password = password, email = email)
            user.put()
            self.redirect("/")

app = main.webapp2.WSGIApplication([
    ('/signup', SignupHandler)
], debug=True)