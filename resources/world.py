# Open Library example API
# =
# "https://openlibrary.org/api/books?bibkeys=ISBN:0451526538&callback=mycallback"

 # default output of Open Library API is javascript, so change the format to JSON. 
 # Start with get route, for a specific ISBN, then make the ISBN a variable.
 # Needs searchability, copyability, but not addition and deletion.

import models

from flask import request, jsonify, Blueprint, redirect, url_for
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user, login_required
from playhouse.shortcuts import model_to_dict


@world.route('/', methods=['GET'])
def get_world_api():
	# books = models.Book.select()
	# print(books)
	# book_dicts = [model_to_dict(b) for b in books]
	# all_books = list(book_dicts)
	# return jsonify(data=all_books), 200

