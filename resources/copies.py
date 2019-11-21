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


#one copy show route
@copy.route('/<id>', methods=['GET'])
def get_one_copy(id):
	copy = models.Copy.get_by_id(id)
	print(copy)
	copy_dict = model_to_dict(copy)
	copy_dict['owner'].pop('password')
	copy_dict['owner'].pop('email')
	return jsonify(data=copy_dict, status={"code": 200, 'message':'Found copy with id{}'.format(copy.id)})

#copy change owner route


#copy delete route
@copy.route('/<id>', methods=['Delete'])
@login_required
def delete_copy(id):
	copy_to_delete = models.Copy.get_by_id(id)
	if (copy_to_delete.owner.id != current_user.id):
		return jsonify(data="Forbidden", status={'code': 403, 'message':"Users can only delete their own books"}), 403
	else:
		copy_to_delete.delete_instance()
		return jsonify(data='resource Successfully deleted', status={"code": 200, "message": "resource deleted"})












