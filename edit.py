import main, wikidb, time, logging
from google.appengine.ext import db

class EditHandler(main.Handler):
    def get(self, *args):
        title = args[0][1:]
        self.render("_edit.html", title = title)

    def post(self, *args):
        title = self.request.get("title")
        content = self.request.get("content")
        entry = wikidb.Entry(title = title, content = content)
        entry.put()
        time.sleep(0.1)
        self.redirect("/" + title)

PAGE_RE = r'(/(?:[a-zA-Z0-9_-]+/?)*)?'
app = main.webapp2.WSGIApplication([
    ('/_edit' + PAGE_RE, EditHandler)
], debug=True)