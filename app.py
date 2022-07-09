from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify
from sqlalchemy import Integer, Text, Date
import json
import datetime

from data import offers_json, orders_json, users_json


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(Integer, primary_key=True)
    first_name = db.Column(Text(50))
    last_name = db.Column(Text(50))
    age = db.Column(Integer)
    email = db.Column(Text(100))
    role = db.Column(Text(30))
    phone = db.Column(Text(30))

    def user_to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "email": self.email,
            "role": self.role,
            "phone": self.phone
        }


class Offer(db.Model):
    __tablename__ = 'offer'
    id = db.Column(Integer, primary_key=True)
    order_id = db.Column(Integer, db.ForeignKey('order.id'))
    executor_id = db.Column(Integer, db.ForeignKey('user.id'))
    order = db.relationship('Order')
    user = db.relationship('User')

    def offer_to_dict(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "executor_id": self.executor_id
        }


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(Integer, primary_key=True)
    name = db.Column(Text(50))
    description = db.Column(Text)
    start_date = db.Column(Date)
    end_date = db.Column(Date)
    address = db.Column(Text)
    price = db.Column(Integer)
    customer_id = db.Column(Integer, db.ForeignKey('user.id'))
    executor_id = db.Column(Integer, db.ForeignKey('user.id'))

    def order_to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "address": self.address,
            "price": self.price,
            "customer_id": self.customer_id,
            "executor_id": self.executor_id
        }


db.drop_all()
db.create_all()

for user in users_json:
    db.session.add(User(
        id=user["id"],
        first_name=user["first_name"],
        last_name=user["last_name"],
        age=user["age"],
        email=user["email"],
        role=user["role"],
        phone=user["phone"]
    ))

for offer in offers_json:
    db.session.add(Offer(
        id=offer["id"],
        order_id=offer["order_id"],
        executor_id=offer["executor_id"]
    ))

for order in orders_json:
    month_start, day_start, year_start = order["start_date"].split('/')
    month_end, day_end, year_end = order["end_date"].split('/')
    db.session.add(Order(
        id=order["id"],
        name=order["name"],
        description=order["description"],
        start_date=datetime.date(year=int(year_start), month=int(month_start), day=int(day_start)),
        end_date=datetime.date(year=int(year_end), month=int(month_end), day=int(day_end)),
        address=order["address"],
        price=order["price"]
    ))

db.session.commit()


@app.route('/users', methods=["GET", "POST"])
def users_page():
    if request.method == "GET":
        all_users = db.session.query(User).all()
        return jsonify([user.user_to_dict() for user in all_users])

    elif request.method == "POST":
        user = json.loads(request.data)
        add_user = User(
            id=user["id"],
            first_name=user["first_name"],
            last_name=user["last_name"],
            age=user["age"],
            email=user["email"],
            role=user["role"],
            phone=user["phone"]
        )

        db.session.add(add_user)
        db.session.commit()

        return "Пользователь создан"


@app.route('/users/<int:pk>', methods=["GET", "PUT", "DELETE"])
def user_by_pk_page(pk):
    if request.method == "GET":
        user = User.query.get(pk)
        return jsonify(user.user_to_dict())

    elif request.method == "PUT":
        put_user = User.query.get(pk)
        put_user.first_name = "Update_user"

        db.session.add(put_user)
        db.session.commit()
        return jsonify(put_user.user_to_dict())

    elif request.method == "DELETE":
        delete_user = User.query.get(pk)
        db.session.delete(delete_user)
        return "Пользователь удалён"


@app.route('/orders', methods=["GET", "POST"])
def orders_page():
    if request.method == "GET":
        all_orders = db.session.query(Order).all()
        return jsonify([order.order_to_dict() for order in all_orders])
    elif request.method == "POST":
        order = json.loads(request.data)
        month_start, day_start, year_start = order["start_date"].split('/')
        month_end, day_end, year_end = order["end_date"].split('/')
        add_order = Order(
            id=order["id"],
            name=order["name"],
            description=order["description"],
            start_date=datetime.date(year=int(year_start), month=int(month_start), day=int(day_start)),
            end_date=datetime.date(year=int(year_end), month=int(month_end), day=int(day_end)),
            address=order["address"],
            price=order["price"]
        )

        db.session.add(add_order)
        db.session.commit()

        return "Заказ создан"


@app.route('/orders/<int:pk>', methods=["GET", "PUT", "DELETE"])
def order_by_pk_page(pk):
    if request.method == "GET":
        order = Order.query.get(pk)
        return jsonify(order.order_to_dict())

    elif request.method == "PUT":
        put_order = Order.query.get(pk)
        put_order.name = "Update_order"

        db.session.add(put_order)
        db.session.commit()
        return jsonify(put_order.order_to_dict())

    elif request.method == "DELETE":
        delete_order = Order.query.get(pk)
        db.session.delete(delete_order)
        return "Заказ удалён"


@app.route('/offers', methods=["GET", "POST"])
def offers_page():
    if request.method == "GET":
        all_offers = db.session.query(Offer).all()
        return jsonify([offer.order_to_dict() for offer in all_offers])

    elif request.method == "POST":
        offer = json.loads(request.data)
        add_offer = Offer(
            id=offer["id"],
            order_id=offer["order_id"],
            executor_id=offer["executor_id"]
        )

        db.session.add(add_offer)
        db.session.commit()

        return "Предложение создано"


@app.route('/offers/<int:pk>', methods=["GET", "PUT", "DELETE"])
def offers_by_pk_page(pk):
    if request.method == "GET":
        offer = Offer.query.get(pk)
        return jsonify(offer.offer_to_dict())

    elif request.method == "PUT":
        put_offer = Offer.query.get(pk)
        put_offer.order_id = 777

        db.session.add(put_offer)
        db.session.commit()
        return jsonify(put_offer.offer_to_dict())

    elif request.method == "DELETE":
        delete_offer = Offer.query.get(pk)
        db.session.delete(delete_offer)
        return "Предложение удалено"


if __name__ == '__main__':
    app.run(debug=True)
