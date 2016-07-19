import webapp2
from google.appengine.ext import db

class Entry(db.Model):
    title = db.StringProperty(required = False)
    content = db.TextProperty(required = False)
    created = db.DateTimeProperty(auto_now_add = True)

class Users(db.Model):
    username = db.StringProperty(required = True)
    password = db.StringProperty(required = True)
    salt = db.StringProperty(required = False)
    email = db.EmailProperty(required = False)

