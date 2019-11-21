import models

from flask import request, jsonify, Blueprint, redirect, url_for
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user, login_required
from playhouse.shortcuts import model_to_dict

trades = Blueprint('trades', 'trades')


##CREATE TRADE ROUTE
#current user(from_user) sends trade request to (to_user)
#if (to_user) accepts, 
	#accepted to true
	#Datefield == accepted date
	#change copy.owner.id to current_user.id
#else
	#send message to (from_user) trade is denied
	
##TRADE FIELDS##
# copy = ForeignKeyField(Copy, backref='')
# from_user = ForeignKeyField(User, backref='')
# to_user = ForeignKeyField(User, backref='')
# accepted = BooleanField()
# traded = DateField()



