from oauth2client.appengine import CredentialsNDBProperty
from google.appengine.ext import ndb


# this class has a predefined name, and is used to store google credentials
class CredentialsModel(ndb.Model):
    credentials = CredentialsNDBProperty(indexed=False)