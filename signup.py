import main, wikidb, utils, logging, re


class SignupHandler(main.Handler):
    def get(self):
        self.render("signup.html")

    def valid_username(self, username):
        USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        return username and USER_RE.match(username)

    def valid_password(self, password):
        PASS_RE = re.compile(r"^.{3,20}$")
        return password and PASS_RE.match(password)

    def valid_verify_password(self, verify):
        VERIFYPASS_RE = re.compile(r"^.{3,20}$")
        return verify and VERIFYPASS_RE.match(verify)

    def valid_email(self, email):
        EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
        return not email or EMAIL_RE.match(email)

    def validate(self, username, password, verify, email):
        if not self.valid_username(username):
            self.error = True

        if not self.valid_password(password):
            self.error = True
        elif password != verify:
            self.error = True

        if not self.valid_email(email):
            self.error = True

        return	self.error

    def get_params(self):
        return self.params

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")
        if self.validate(username, password, verify, email) and not utils.get_userdb_cache(username):
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
        else:
            self.render("signup.html", error="invalid data")

app = main.webapp2.WSGIApplication([
    ('/signup', SignupHandler)
], debug=True)