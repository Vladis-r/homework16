import json
import datetime
from flask import Blueprint, request, jsonify

from app import db
from db_init import User, Order, Offer

routes_Blueprint = Blueprint('routes_blueprint', __name__)


@routes_Blueprint.route('/users', methods=["GET", "POST"])
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


@routes_Blueprint.route('/users/<int:pk>', methods=["GET", "PUT", "DELETE"])
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


@routes_Blueprint.route('/orders', methods=["GET", "POST"])
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


@routes_Blueprint.route('/orders/<int:pk>', methods=["GET", "PUT", "DELETE"])
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


@routes_Blueprint.route('/offers', methods=["GET", "POST"])
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


@routes_Blueprint.route('/offers/<int:pk>', methods=["GET", "PUT", "DELETE"])
def users_page(pk):
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
