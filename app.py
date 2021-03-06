import os
from flask import Flask, jsonify, g
from flask_cors import CORS
from flask_login import LoginManager

from resources.users import users
from resources.books import books
from resources.copies import copy
from resources.trades import trades

import models

DEBUG = True
PORT = 8000

app = Flask(__name__)

app.secret_key = "super sneaky secret key"

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(userid):
	try:
		return models.User.get(models.User.id == userid)
	except models.DoesNotExist:
		return None

@login_manager.unauthorized_handler
def unauthorized():
	return jsonify(data={'error':'You must be logged in to view this page'}, status={'code':401, 'message':'You must be logged in to access that resource'}), 401

@app.before_request
def before_request():
	#connect to db before each request
	g.db = models.DATABASE
	g.db.connect()

@app.after_request
def after_request(response):
	#closes db connection after each request
	g.db.close()
	return response



CORS(users, origins=['http://localhost:3000', 'https://thelibrarium.herokuapp.com'], supports_credentials=True)
CORS(books, origins=['http://localhost:3000', 'https://thelibrarium.herokuapp.com'], supports_credentials=True)
CORS(copy, origins=['http://localhost:3000', 'https://thelibrarium.herokuapp.com'], supports_credentials=True)
CORS(trades, origins=['http://localhost:3000', 'https://thelibrarium.herokuapp.com'], supports_credentials=True)

app.register_blueprint(users, url_prefix='/api/v1/users')
app.register_blueprint(books, url_prefix='/api/v1/books')
app.register_blueprint(copy, url_prefix='/api/v1/copies')
app.register_blueprint(trades, url_prefix='/api/v1/trades')



if 'ON_HEROKU' in os.environ:
	print('\non heroku!')
	models.initialize()


if __name__ == '__main__':
	models.initialize()
	app.run(debug=DEBUG, port=PORT)

























