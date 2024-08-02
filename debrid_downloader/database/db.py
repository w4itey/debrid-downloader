from peewee import *
from playhouse.db_url import connect

db = connect('sqlite:///default.db')

class ingest(Model):

    filename = CharField()
    hash = CharField()
    magnet = TextField()

    class Meta:
        database = db 