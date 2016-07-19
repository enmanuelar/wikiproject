import main, wikidb, time, logging
from google.appengine.ext import db


class EditHandler(main.Handler):
    def get(self, *args):
        title = args[0][1:]
        entity = db.Query(wikidb.Entry).filter('title =', title).get()
        if entity and self.request.cookies.get('name'):
            self.render("_edit.html",title=entity.title, content=entity.content, new_page=False)
        elif not entity and self.request.cookies.get('name'):
            self.render("_edit.html", title = title, new_page = True)
        else:
            self.redirect("/login")

    def post(self, *args):
        url = self.request.url
        title = url.split('/')[-1]
        content = self.request.get("content")
        entity = db.Query(wikidb.Entry).filter('title =', title).get()
        if entity:
            entity.content = content
            entity.put()
        else:
            entry = wikidb.Entry(title = title, content = content)
            entry.put()
        time.sleep(0.1)
        self.redirect("/" + title)

PAGE_RE = r'(/(?:[a-zA-Z0-9_-]+/?)*)?'
app = main.webapp2.WSGIApplication([
    ('/_edit' + PAGE_RE, EditHandler)
], debug=True)