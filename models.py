from peewee import *
from flask_login import UserMixin
import datetime


DATABASE = SqliteDatabase('librarium.sqlite')

class User(UserMixin, Model):
	uname = CharField(unique = True)
	pword = CharField()
	email = CharField()

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
	book = ForeignKeyField(Book, backref='books')
	owner = ForeignKeyField(User, backref='')
	hardcover = BooleanField()

	class Meta:
		database = DATABASE

class Trade(Model):
	copy_id = ForeignKeyField(Copy, backref='')
	current_o = ForeignKeyField(User, backref='')
	former_o = ForeignKeyField(User, backref='')
	traded = DateField()

	class Meta:
		database = DATABASE


def initialize():
	DATABASE.connect()
	DATABASE.create_tables([User, Book, Copy, Trade], safe=True)
	print("TABLES Created")
	DATABASE.close()







