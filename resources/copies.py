import models

from flask import request, jsonify, Blueprint
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user
from playhouse.shortcuts import model_to_dict

copy = Blueprint('copies', 'copy')


# @copy.route('/', method=['POST'])
# @login_reuired
# def create_copy():
# 	payload = request.get_json()
# 	try:
		













