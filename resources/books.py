import models

from flask import request, jsonify, Blueprint
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user
from playhouse.shortcuts import model_to_dict

books = Blueprint('books', 'books')

#books create route
@books.route('/', methods=['POST'])
def create_book():
	payload = request.get_json()

	try:
		models.Book.get(models.Book.isbn == payload['isbn'])
		return jsonify(data={}, status={'code': 401, 'message':'A book with this isbn already exists'}), 401
	except models.DoesNotExist:
		book = models.Book.create(**payload)
		print(book.__dict__)
		print(model_to_dict(book), 'model to dict')
		book_dict = model_to_dict(book)
		return jsonify(data=book_dict, status={"code": 201, "message": "Success"}), 201

#show page for all books
@books.route('/', methods=['GET'])
def get_all_books():
	books = models.Book.select()
	print(books)

	book_dicts = [model_to_dict(b) for b in books]

	all_books = list(book_dicts)
	return jsonify(data=all_books), 200
















