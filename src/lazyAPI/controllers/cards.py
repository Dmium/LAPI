from lazyAPI import app, db, mongo

from flask import jsonify, request

from lazyAPI.models import card
from lazyAPI.models.card import Card

from lazyAPI.schemas import card_schema, card_balanceonly_schema

@app.route('/cards', methods=['POST'])
def cards_buy():
    request_dict = request.get_json()
    card = Card(balance=request_dict['balance'], passenger_id=request_dict['passenger']['id'])
    db.session.add(card)
    db.session.commit()
    request_dict['_id'] = card.id
    mongo.db.cards.insert_one(request_dict)
    return jsonify(
        card_schema.Card_Schema().dump(
            card
        ).data
    )

@app.route('/cards/<cid>', methods=['GET'])
def cards_get(cid):
    mongo.db.cards.find_one({"_id": int(cid)})
    return jsonify(card_schema.Card_Schema().dump(Card.query.filter_by(id = cid).first()).data)

@app.route('/cards/', methods=['GET'])
def cards_get_all():
    mongo.db.cards.find()
    return jsonify(card_schema.Card_Schema(many=True).dump(Card.query.all()).data)

@app.route('/cards/<cid>/balance', methods=['GET'])
def cards_get_balance(cid):
    # balance seems kinda unimportant when we have get card
    mongo.db.cards.find_one({"_id": int(cid)})
    return jsonify(card_balanceonly_schema.Card_Schema().dump(Card.query.filter_by(id = cid).first()).data)

@app.route('/cards/<cid>', methods=['PUT'])
def cards_update(cid): # replace appropriate fields
    request_dict = request.get_json()
    mongo.db.cards.update_one({'_id':int(cid)}, {"$set": request_dict})
    card = Card.query.get(cid)
    card.balance=request_dict['balance']
    card.passenger_id=request_dict['passenger']['id']
    db.session.commit()
    return jsonify(
        card_schema.Card_Schema().dump(
            card
        ).data
    )
