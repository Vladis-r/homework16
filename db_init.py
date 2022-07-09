# import datetime
# from sqlalchemy import Integer, Text, Date
#
# from data import offers_json, orders_json, users_json
# from app import db
#
#
#
#
# class User(db.Model):
#     __tablename__ = 'user'
#     id = db.Column(Integer, primary_key=True)
#     first_name = db.Column(Text(50))
#     last_name = db.Column(Text(50))
#     age = db.Column(Integer)
#     email = db.Column(Text(100))
#     role = db.Column(Text(30))
#     phone = db.Column(Text(30))
#
#     def user_to_dict(self):
#         return {
#             "id": self.id,
#             "first_name": self.first_name,
#             "last_name": self.last_name,
#             "age": self.age,
#             "email": self.email,
#             "role": self.role,
#             "phone": self.phone
#         }
#
#
# class Offer(db.Model):
#     __tablename__ = 'offer'
#     id = db.Column(Integer, primary_key=True)
#     order_id = db.Column(Integer, db.ForeignKey('order.id'))
#     executor_id = db.Column(Integer, db.ForeignKey('user.id'))
#     order = db.relationship('Order')
#     user = db.relationship('User')
#
#     def offer_to_dict(self):
#         return {
#             "id": self.id,
#             "order_id": self.order_id,
#             "executor_id": self.executor_id
#         }
#
#
# class Order(db.Model):
#     __tablename__ = 'order'
#     id = db.Column(Integer, primary_key=True)
#     name = db.Column(Text(50))
#     description = db.Column(Text)
#     start_date = db.Column(Date)
#     end_date = db.Column(Date)
#     address = db.Column(Text)
#     price = db.Column(Integer)
#     customer_id = db.Column(Integer, db.ForeignKey('user.id'))
#     executor_id = db.Column(Integer, db.ForeignKey('user.id'))
#
#     def order_to_dict(self):
#         return {
#             "id": self.id,
#             "name": self.name,
#             "description": self.description,
#             "start_date": self.start_date,
#             "end_date": self.end_date,
#             "address": self.address,
#             "price": self.price,
#             "customer_id": self.customer_id,
#             "executor_id": self.executor_id
#         }
#
#
# db.drop_all()
# db.create_all()
#
# for user in users_json:
#     db.session.add(User(
#         id=user["id"],
#         first_name=user["first_name"],
#         last_name=user["last_name"],
#         age=user["age"],
#         email=user["email"],
#         role=user["role"],
#         phone=user["phone"]
#     ))
#
# for offer in offers_json:
#     db.session.add(Offer(
#         id=offer["id"],
#         order_id=offer["order_id"],
#         executor_id=offer["executor_id"]
#     ))
#
# for order in orders_json:
#     month_start, day_start, year_start = order["start_date"].split('/')
#     month_end, day_end, year_end = order["end_date"].split('/')
#     db.session.add(Order(
#         id=order["id"],
#         name=order["name"],
#         description=order["description"],
#         start_date=datetime.date(year=int(year_start), month=int(month_start), day=int(day_start)),
#         end_date=datetime.date(year=int(year_end), month=int(month_end), day=int(day_end)),
#         address=order["address"],
#         price=order["price"]
#     ))
#
# db.session.commit()
