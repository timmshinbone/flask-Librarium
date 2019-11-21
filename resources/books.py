import models

from flask import request, jsonify, Blueprint, redirect, url_for
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user, login_required
from playhouse.shortcuts import model_to_dict

books = Blueprint('books', 'books')

#books create route
@books.route('/', methods=['POST'])
@login_required
def create_book():
	payload = request.get_json()

	try:
		book = models.Book.get(models.Book.isbn == payload['isbn'])
		print(book, "this is book")
		# return jsonify(data={}, status={'code': 401, 'message':'A book with this isbn already exists, create copy?'}), 401
		return redirect(url_for('copies.create_copy', id=book), code=302)
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

#show one book
@books.route('/<id>', methods=['GET'])
def get_one_book(id):
	book = models.Book.get_by_id(id)
	book_dict = model_to_dict(book)
	return jsonify(data=book_dict, status={"code": 200, 'message':'Found book with id{}'.format(book.id)})


#edit book info(user number 1 only)
@books.route('/<id>', methods=['PUT'])
@login_required
def update_book(id):
	payload = request.get_json()
	book = models.Book.get_by_id(id)

	if(current_user.id == 1):
		book.title = payload['title'] if 'title' in payload else None
		book.author = payload['author'] if 'author' in payload else None
		book.isbn = payload['isbn'] if 'isbn' in payload else None
		book.genre = payload['genre'] if 'genre' in payload else None
		book.pages = payload['pages'] if 'pages' in payload else None
		book.image = payload['image'] if 'image' in payload else None
		book.published = payload['published'] if 'published' in payload else None
		book.save()

		book_dict = model_to_dict(book)
		print(book_dict)
		return jsonify(data=book_dict, status={"code": 200, "message": "Success"})
	else:
		return jsonify(data="Forbidden", status={'code': 403, 'message':"You are not authorized to edit book information"}), 403





