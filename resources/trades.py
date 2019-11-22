import models

from flask import request, jsonify, Blueprint, redirect, url_for
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user, login_required
from playhouse.shortcuts import model_to_dict

trades = Blueprint('trades', 'trades')



#make a trade "ticket"
@trades.route('/<f>/<t>', methods=['POST'])
@login_required
def make_trade_request(f, t):
	payload = request.get_json()
	
	payload['from_user'] = current_user.id
	payload['copy_from'] = models.Copy.get_by_id(f)
	payload['copy_to'] = models.Copy.get_by_id(t)
	payload['to_user'] = models.User.get_by_id(payload['copy_to'].owner_id)

	trade = models.Trade.create(**payload)
	trade_dict = model_to_dict(trade)

	return jsonify(data=trade_dict, status={"code":201, "message": "Success"}), 201




##CREATE TRADE ROUTE (POST) with update queries

#if (to_user) accepts, 
	#call copy owner change function from copies
	#copy_xchange = models.Copy.change_owner(owner=current_user.id)
#else
	#send message to (from_user) trade is denied
#accept or deny trade ticket
@trades.route('/<id>', methods=['PUT'])
@login_required
def trade_decider(id):
	payload = request.get_json()
	trade = models.Trade.get_by_id(id)
	trade_dict = model_to_dict(trade)
	##REMOVES SENSITIVE INFO##
	trade_dict['copy_from']['owner'].pop('password')
	trade_dict['copy_from']['owner'].pop('email')
	trade_dict['copy_to']['owner'].pop('password')
	trade_dict['copy_to']['owner'].pop('email')
	trade_dict['from_user'].pop('password')
	trade_dict['from_user'].pop('email')
	trade_dict['to_user'].pop('password')
	trade_dict['to_user'].pop('email')
	##^^REMOVES SENSITIVE INFO^^##
	from_user = trade_dict['from_user']
	# print("THIS IS from_user", from_user)
	copy_from = trade_dict['copy_from']
	# print("THIS IS copy_from", copy_from)
	to_user = trade_dict['to_user']
	copy_to = trade_dict['copy_to']

	print("THIS IS copy_to (Taylor)", copy_to) # copy that belongs to taylor
	print("THIS IS copy_from (timm) ", copy_from) # copy that belongs to timm

	print('trade.to_user (taylor)', trade.to_user.username) # taylor (2)
	print('trade.from_user(timm)', trade.from_user.username) #timm (1)
	if(payload['status'] == "accepted"):
		query1 = models.Copy.update(owner=trade.to_user).where(models.Copy.id == copy_from['id'])
		query1.execute()
		query2 = models.Copy.update(owner=trade.from_user).where(models.Copy.id == copy_to['id'])
		query2.execute()
		# copy_to_record = models.Copy.get(models.Copy.id == copy_to['id'])
		# copy_from_record = models.Copy.get(models.Copy.id == copy_from['id'])

		# copy_to_record.owner = 

		# .save()


		trade_status = models.Trade.update(status="accepted")
		trade_status.execute()
		print("this is trade status", trade_dict['status'])
		#update the from_copy.owner to to_user
		#update the to_copy.owner to from_user
	return jsonify(data=trade_dict, status={"code":200, "message": "Success"}), 200





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

#trade show one route
@trades.route('/<id>', methods=['GET'])
def show_one_trade(id):
	trade = models.Trade.get_by_id(id)
	print(trade, "this is trade")
	trade_dict = model_to_dict(trade)
	trade_dict['copy_from']['owner'].pop('password')
	trade_dict['copy_from']['owner'].pop('email')
	trade_dict['copy_to']['owner'].pop('password')
	trade_dict['copy_to']['owner'].pop('email')
	trade_dict['from_user'].pop('password')
	trade_dict['from_user'].pop('email')
	trade_dict['to_user'].pop('password')
	trade_dict['to_user'].pop('email')
	return jsonify(data=trade_dict, status={"code": 200, 'message':'Found copy with id{}'.format(trade.id)})

#trade delete route
@trades.route('/<id>', methods=['Delete'])
@login_required
def delete_trade(id):
	trade_to_delete = models.Trade.get_by_id(id)
	if (current_user.id != 1):
		return jsonify(data="Forbidden", status={'code': 403, 'message':"you are not authorized to delete trades"}), 403
	else:
		trade_to_delete.delete_instance()
		return jsonify(data='resource Successfully deleted', status={"code": 200, "message": "resource deleted"})
















