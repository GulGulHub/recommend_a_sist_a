# from flask_sqlalchemy import SQLAlchemy
# from flask_login import UserMixin
# from datetime import datetime
#
#
#
#
#
#
# class User(UserMixin, db.Model):
#     __tablename__ = 'users'
#
#     id = db.Column(db.Integer, primary_key=True)
#     full_name = db.Column(db.String(200), nullable=False)  # i.e Hanna Barbera
#     display_name = db.Column(db.String(20), unique=True, nullable=False)  # i.e hanna_25
#     email = db.Column(db.String(120), unique=True, nullable=False)  # i.e hanna@hanna-barbera.com
#     password = db.Column(db.String(32), nullable=False)
#     created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#     is_authenticated = db.Column(db.Boolean, nullable=False)
#     is_active = db.Column(db.Boolean, nullable=False)
#     is_anonymus = db.Column(db.Boolean, nullable=False)
#
#
#
#     @classmethod
#     def get_id(cls, user_id):
#         return cls.query.filter_by(id=user_id).first()
#
#     def __repr__(self):
#         return f"User({self.id}, '{self.display_name}', '{self.email}')"
#
#     def insert(self):
#         db.session.add(self)
#         db.session.commit()
#
#     def delete(self):
#         db.session.delete(self)
#         db.session.commit()
#
#     def update(self):
#         db.session.commit()



    # def __init__(self, id, username, email, password):
    #     self.id = id
    #     self.username = username
    #     self.email = email
    #     self.password = password
    #     self.is_logged_in = False
    #     self.image = []
    #
    # def sign_up(self):
    #     pass
    #     # create database and add all info
    #
    # def log_in(self):
    #     pass
    #     # compare with db and see if log in is successfull, then is_logged in = True
    #
    # def recommend_user(self):
    #     pass
    #     # add a user
    #
    # def add_business(self):
    #     pass
    #     # add a business


# class Students(db.Model):
#    id = db.Column('student_id', db.Integer, primary_key = True)
#    name = db.Column(db.String(100))
#    city = db.Column(db.String(50))
#    addr = db.Column(db.String(200))
#    pin = db.Column(db.String(10))
#
#    def __init__(self, name, city, addr,pin):
#        self.name = name
#        self.city = city
#        self.addr = addr
#        self.pin = pin