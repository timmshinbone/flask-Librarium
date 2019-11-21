import models

from flask import request, jsonify, Blueprint
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user, login_required
from playhouse.shortcuts import model_to_dict

copy = Blueprint('copies', 'copy')

#make a copy
@copy.route('/', methods=['POST'])
@login_required
def create_copy():
	payload = request.get_json()
	c_info = models.Book.get(models.Book.isbn == payload['isbn'])
	print(c_info, "this is c_info")
	copy = models.Copy.create(book=c_info, owner=current_user.id)
	copy_dict = model_to_dict(copy)
	return jsonify(data=copy_dict, status={"code":201, "message": "Success"}), 201


#all copies show route
@copy.route('/', methods=['GET'])
def get_all_copies():
	copies = models.Copy.select()
	print(copies)
	copy_dicts = [model_to_dict(c) for c in copies]
	all_copies = list(copy_dicts)
	return jsonify(data=all_copies), 200








