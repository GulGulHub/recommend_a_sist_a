from flask_login import UserMixin
from datetime import datetime
import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

'''
setup_db(app):
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app):
    # database_path = os.getenv('DATABASE_URL', 'DATABASE_URL_WAS_NOT_SET?!')
    #
    # # https://stackoverflow.com/questions/62688256/sqlalchemy-exc-nosuchmoduleerror-cant-load-plugin-sqlalchemy-dialectspostgre
    # database_path = database_path.replace('postgres://', 'postgresql://')

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
    app.config['SECRET_KEY'] = "DxoTNR5WqA4MmgYk"
    db.app = app
    db.init_app(app)

'''
    drops the database tables and starts fresh
    can be used to initialize a clean database
'''
def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(200), nullable=False)  # i.e Hanna Barbera
    display_name = db.Column(db.String(20), unique=True, nullable=False)  # i.e hanna_25
    email = db.Column(db.String(120), unique=True, nullable=False)  # i.e hanna@hanna-barbera.com
    password = db.Column(db.String(32), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)



    @classmethod
    def get_by_id(cls, user_id):
        return cls.query.filter_by(id=user_id).first()

    def __repr__(self):
        return f"User({self.id}, '{self.display_name}', '{self.email}')"

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()


@classmethod
def get_id(cls, user_id):
    return cls.query.filter_by(id=user_id).first()
