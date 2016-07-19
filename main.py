#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2, os, jinja2, wikidb, logging, utils
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


class MainPage(Handler):
    def get(self):
        user_cookie = self.request.cookies.get('name')
        html = '<a href="/signup">signup</a> | <a href="/login">login</a>'
        if user_cookie:
            user_id = int(self.request.cookies.get('user_id'))
            entity = wikidb.Users.get_by_id(user_id)
            valid_hash = utils.check_secure_val(user_cookie, entity.username)
            if valid_hash:
                html = '%s | <a href="/logout">logout</a>' % entity.username
        entries = db.GqlQuery("SELECT * FROM Entry ORDER BY created DESC LIMIT 10")
        self.render("index.html", entries=entries, html=html)



class WikiPageHandler(Handler):
    def get(self, *args):
        entity = db.Query(wikidb.Entry).filter('title =', args[0][1:]).get()
        if entity:
            self.render("/page.html",title=entity.title, content=entity.content)
        else:
            if self.request.cookies.get('name'):
                self.redirect("/_edit" + args[0])
            else:
                self.redirect("/login")

    def post(self, *args):
        content = self.request.get("content")
        entity = db.Query(wikidb.Entry).filter('title =', args[0][1:]).get()
        entity.content = content
        entity.put()

class LoginHandler(Handler):
    def get(self):
        self.render("login.html")

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        entity = db.Query(wikidb.Users).filter('username =', username).get()
        if entity:
            if utils.validpw(password, entity.salt, entity.password):
                hash_cookie = "%s|%s" % (entity.password, entity.salt)
                id_cookie = str(entity.key().id())
                self.response.headers.add_header('Set-Cookie', 'name=%s; Path=/' % (str(hash_cookie)))
                self.response.headers.add_header('Set-Cookie', 'user_id=%s; Path=/' % id_cookie)
                self.redirect("/")
        self.render("login.html", error="invalid login")

class LogoutHandler(Handler):
    def get(self):
        self.response.delete_cookie('name')
        self.response.delete_cookie('user_id')
        self.redirect("/")

PAGE_RE = r'(/(?:[a-zA-Z0-9_-]+/?)*)?'
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/login', LoginHandler),
    ('/logout', LogoutHandler),
    (PAGE_RE, WikiPageHandler)

], debug=True)
