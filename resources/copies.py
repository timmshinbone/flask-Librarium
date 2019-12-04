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
	print(copies, "this is copies")
	copy_dicts = [model_to_dict(c) for c in copies]
	print("THIS IS COPY_DICTS --->", copy_dicts)
	#remove password and email from json return data
	[x['owner'].pop('password') for x in copy_dicts]
	[x['owner'].pop('email') for x in copy_dicts]
	# all_copies = list(copy_dicts)
	# print("THIS IS ALL COPIES ====>>", all_copies)
	
	return jsonify(data=copy_dicts), 200


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
@copy.route('/<id>', methods=['PUT'])
@login_required
def change_owner(id):
	payload = request.get_json()
	copy = models.Copy.get_by_id(id)
	print(copy)
	if(current_user.id == copy.owner.id):
		copy.owner = payload['id']
		copy_dict = model_to_dict(copy)
		copy_dict['owner'].pop('password')
		copy_dict['owner'].pop('email')
		return jsonify(data=copy_dict, status={"code": 200, "message": "Success"})
	else:
		return jsonify(data="Forbidden", status={'code': 403, 'message':"Users can only update their own copies"}), 403

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





















