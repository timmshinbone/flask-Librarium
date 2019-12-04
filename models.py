import os
from peewee import *
from flask_login import UserMixin
import datetime
from playhouse.db_url import connect



if 'ON_HEROKU' in os.environ:
	DATABASE = connect(os.environ.get('DATABASE_URL'))
else:
	DATABASE = SqliteDatabase('librarium.sqlite')

class User(UserMixin, Model):
	username = CharField(unique = True)
	password = CharField()
	email = CharField(unique = True)

	class Meta:
		database = DATABASE

class Book(Model):
	title = CharField()
	author = CharField()
	isbn = CharField(unique = True)
	genre = CharField()
	pages = IntegerField()
	image = CharField()
	published = CharField()

	class Meta:
		database = DATABASE

class Copy(Model):
	book = ForeignKeyField(Book, backref='copies')
	owner = ForeignKeyField(User, backref='copies')

	class Meta:
		database = DATABASE

class Trade(Model):
	copy_from = ForeignKeyField(Copy, backref='trades')
	from_user = ForeignKeyField(User, backref='trades')
	copy_to = ForeignKeyField(Copy, backref='trades')
	to_user = ForeignKeyField(User, backref='trades')
	# accepted = BooleanField()
	trade_date = DateField(default=datetime.datetime.now())
	status = CharField(default='pending')

	class Meta:
		database = DATABASE


def initialize():
	DATABASE.connect()
	DATABASE.create_tables([User, Book, Copy, Trade], safe=True)
	print("TABLES Created")
	DATABASE.close()	







