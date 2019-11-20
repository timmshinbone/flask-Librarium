import models

from flask import request, jsonify, Blueprint
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user
from playhouse.shortcuts import model_to_dict

users = Blueprint('users', 'users')

#Registration route
@users.route('/register', methods=['POST'])
def register():
	payload = request.get_json()
	payload['email'].lower()

	try:
		try:
			models.User.get(models.User.email == payload['email'])
			return jsonify(data={}, status={'code': 401, 'message':'A user with this email already exists'}), 401
		except:
			models.User.get(models.User.username == payload['username'])
			return jsonify(data={}, status={'code': 401, 'message':'A user with this username already exists'}), 401
	except models.DoesNotExist:
		payload['password'] = generate_password_hash(payload['password'])
		user = models.User.create(**payload)

		login_user(user)

		user_dict = model_to_dict(user)
		print(user_dict)

		del user_dict['password']

		return jsonify(data=user_dict, status={'code': 201, 'message':'Successfully Registered {}'.format(user_dict['username'])}), 201


#login route
@users.route('/login', methods=['POST'])
def login():
	payload = request.get_json()

	try:
		user = models.User.get(models.User.username == payload['username'])
		user_dict = model_to_dict(user)

		if(check_password_hash(user_dict['password'], payload['password'])):
			login_user(user)
			del user_dict['password']
			return jsonify(data=user_dict, status={'code':200, 'message': "Successfully logged in {}".format(user_dict['username'])}), 200
		else:
			print("uh uh uh, you didn't say the magic word")
			return jsonify(data={}, status={'code': 401, 'message':'Username of Password is incorrect'}), 401
	except models.DoesNotExist:
		print('user not found')
		return jsonify(data={}, status={'code': 401, 'message':'User not found'}), 401

#user lists - do not display sensitive info(email and password)
@users.route('/', methods=['GET'])
def list_users():
	users = models.User.select()
	print(users)

	user_dicts = [model_to_dict(u) for u in users]
	def remove_doxx(u):
		u.pop('password')
		u.pop('email')
		return u

	user_dicts_without_doxx = list(map(remove_doxx, user_dicts))
	return jsonify(data=user_dicts_without_doxx), 200

@users.route('/logged_in', methods=['GET'])
def get_logged_in_user():
	if not current_user.is_authenticated:
		return jsonify(data={}, status={'code': 401, 'message':"No user is currently logged in"}), 401
	else:
		print(current_user)
		print(model_to_dict(current_user))
		user_dict = model_to_dict(current_user)
		user_dict.pop('password')
		user_dict.pop('email')
		return jsonify(user_dict)

@users.route('/logout', methods=['GET'])
def logout():
	username = model_to_dict(current_user)['username']
	logout_user()
	return jsonify(data={}, status={'code': 200, 'message': "Successfully logged out {}".format(username)})




















