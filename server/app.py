#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, abort
from flask_migrate import Migrate
from sqlalchemy import desc
from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries', methods=['GET'])
def bakeries():
    try:
        bakeries = Bakery.query.all()

        bakery_data = [{
            "id": bakery.id,
            "name": bakery.name,
            "created_at": bakery.created_at.strftime('%Y-%m-%d %H:%M:%S') if bakery.created_at else None,
            "updated_at": bakery.updated_at.strftime('%Y-%m-%d %H:%M:%S') if bakery.updated_at else None
        } for bakery in bakeries]

        response = make_response(jsonify(bakery_data), 200)
        response.headers['Content-Type'] = 'application/json'

        return response

    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

@app.route('/bakeries/<int:id>', methods=['GET'])
def get_bakery_by_id(id):
    bakery = db.session.query(Bakery).get(id)
    
    if bakery is None:
        response = make_response(jsonify({"error": "Bakery not found"}), 404)
        return response
    
    bakery_data = {
        "id": bakery.id,
        "name": bakery.name,
        "created_at": bakery.created_at,
        "updated_at": bakery.updated_at,
        "baked_goods": [{"id": bg.id, "name": bg.name, "price": bg.price} for bg in bakery.baked_goods]
    }
    
    response = make_response(jsonify(bakery_data), 200)
    return response

@app.route('/baked_goods/by_price', methods=['GET'])
def baked_goods_by_price():
    try:
        baked_goods = BakedGood.query.order_by(desc(BakedGood.price)).all()

        data = [{
            "id": item.id,
            "name": item.name,
            "price": item.price,
            "created_at": item.created_at.strftime('%Y-%m-%d %H:%M:%S') if item.created_at else None,
            "updated_at": item.updated_at.strftime('%Y-%m-%d %H:%M:%S') if item.updated_at else None
        } for item in baked_goods]

        response = make_response(jsonify(data), 200)
        response.headers['Content-Type'] = 'application/json'

        return response

    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    try:
        baked_good = BakedGood.query.order_by(desc(BakedGood.price)).first()

        data = {
            "id": baked_good.id,
            "name": baked_good.name,
            "price": baked_good.price,
            "created_at": baked_good.created_at.strftime('%Y-%m-%d %H:%M:%S') if baked_good.created_at else None,
            "updated_at": baked_good.updated_at.strftime('%Y-%m-%d %H:%M:%S') if baked_good.updated_at else None
        }

        response = make_response(jsonify(data), 200)
        response.headers['Content-Type'] = 'application/json'

        return response

    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
