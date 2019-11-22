import models

from flask import request, jsonify, Blueprint, redirect, url_for
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user, login_required
from playhouse.shortcuts import model_to_dict

trades = Blueprint('trades', 'trades')


##CREATE TRADE ROUTE (POST) with update queries
#current user(from_user) sends trade request([from_copy] for [to_copy]) to (to_user)
#if (to_user) accepts, 
	#change copy.owner.id to current_user.id
	#copy_xchange = models.Copy.change_owner(owner=current_user.id)
#else
	#send message to (from_user) trade is denied

#make a trade "ticket"
@trades.route('/<f>/<t>', methods=['POST'])
@login_required
def make_trade_request(f, t):
	payload = request.get_json()
	print("this is the payload -->", payload)
	payload['from_user'] = current_user.id
	payload['copy_from'] = models.Copy.get_by_id(f)
	payload['copy_to'] = models.Copy.get_by_id(t)
	payload['to_user'] = models.User.get_by_id(payload['copy_to'].owner_id)

	trade = models.Trade.create(**payload)
	trade_dict = model_to_dict(trade)

	return jsonify(data=trade_dict, status={"code":201, "message": "Success"}), 201

#show all trades
@trades.route('/', methods=['GET'])
def show_all_trades():
	trades = models.Trade.select()
	print(trades, "this is trades")
	trades_dicts = [model_to_dict(t) for t in trades]
	
	[x['copy_from']['owner'].pop('password') for x in trades_dicts]
	[x['copy_from']['owner'].pop('email') for x in trades_dicts]
	[x['copy_to']['owner'].pop('password') for x in trades_dicts]
	[x['copy_to']['owner'].pop('email') for x in trades_dicts]
	[x['from_user'].pop('password') for x in trades_dicts]
	[x['from_user'].pop('email') for x in trades_dicts]
	[x['to_user'].pop('password') for x in trades_dicts]
	[x['to_user'].pop('email') for x in trades_dicts]

	return jsonify(data=trades_dicts), 200



