import hashlib, random, string, wikidb
from google.appengine.api import memcache
from google.appengine.ext import db

## HASHING FUNCTIONS
def make_salt():
    return ''.join(random.choice(string.letters) for x in xrange(5))


def hashpw(password, salt=None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(password + salt).hexdigest()
    return (h, salt)


def validpw(password, salt, compare):
    if hashpw(password, salt)[0] == compare:
        return True


def hash_str(s):
    return hashlib.md5(s).hexdigest()


def hash_cookie(username):
    h = hashpw(username)
    return "%s|%s" % (h[0], h[1])


def check_secure_val(value, username):
    hash_and_salt = value.split('|')
    if validpw(username, hash_and_salt[1], hash_and_salt[0]):
        return True
    else:
        return None

##CACHE
def get_userdb_cache(username):
    entity = memcache.get(username)
    return entity

def add_userdb_cache(username, entity_key):
    memcache.set(username, entity_key)