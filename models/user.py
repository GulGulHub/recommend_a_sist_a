import os
from flask_login import UserMixin
from datetime import datetime
import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.types import UserDefinedType
from geoalchemy2.types import Geometry
from shapely.geometry import Point
from geoalchemy2.shape import to_shape
from geoalchemy2.elements import WKTElement
from geoalchemy2.functions import ST_DWithin
from geoalchemy2.types import Geography
from sqlalchemy.sql.expression import cast
from geoalchemy2.shape import from_shape
from dotenv import load_dotenv   #for python-dotenv method
load_dotenv()                    #for python-dotenv method





db = SQLAlchemy()

'''
setup_db(app):
    binds a flask application and a SQLAlchemy service
'''
MY_SQL_KEY = os.environ.get("MYSQL_KEY")
SUPER_SECRET_KEY = os.environ.get("SECRET_KEY")
def setup_db(app):
    # database_path = os.getenv('DATABASE_URL', 'DATABASE_URL_WAS_NOT_SET?!')
    #
    # # https://stackoverflow.com/questions/62688256/sqlalchemy-exc-nosuchmoduleerror-cant-load-plugin-sqlalchemy-dialectspostgre
    # database_path = database_path.replace('postgres://', 'postgresql://')
    # ols sql db
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root:{MY_SQL_KEY}@localhost/db_users'
    app.config['SECRET_KEY'] = SUPER_SECRET_KEY
    db.app = app
    db.init_app(app)

'''
    drops the database tables and starts fresh
    can be used to initialize a clean database
'''
def db_drop_and_create_all():

    #db.drop_all()
    db.create_all()

    # Initial sample data:
    #insert_sample_locations()

    def insert_sample_locations():
        loc1 = SampleLocation(
            description='Brandenburger Tor',
            geom=SampleLocation.point_representation(
                latitude=52.516247,
                longitude=13.377711
            )
        )
        loc1.insert()

        loc2 = SampleLocation(
            description='Schloss Charlottenburg',
            geom=SampleLocation.point_representation(
                latitude=52.520608,
                longitude=13.295581
            )
        )
        loc2.insert()

        loc3 = SampleLocation(
            description='Tempelhofer Feld',
            geom=SampleLocation.point_representation(
                latitude=52.473580,
                longitude=13.405252
            )
        )
        loc3.insert()


class User(UserMixin, db.Model):
    __tablename__ = 'db_users'

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

class Sister(UserMixin, db.Model):
    __tablename__ = 'db_sisters'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(200), nullable=False)  # i.e Hanna Barbera
    tag_name = db.Column(db.String(20), nullable=False)  # architect, it, massage
    contact = db.Column(db.String(120), nullable=False)  # an email, webpage, phonenumber
    address = db.Column(db.String(32), nullable=False)  # an address in Berlin
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


# class SpatialConstants:
#     SRID = 4326
# class SampleLocation(db.Model):
#     __tablename__ = 'sample_locations'
#
#     id = db.Column(db.Integer, primary_key=True)
#     description = db.Column(db.String(80))
#     geom = db.Column(Geometry(geometry_type='POINT', srid=SpatialConstants.SRID))
#
#     @staticmethod
#     def point_representation(latitude, longitude):
#         point = 'POINT(%s %s)' % (longitude, latitude)
#         wkb_element = WKTElement(point, srid=SpatialConstants.SRID)
#         return wkb_element
#
#     @staticmethod
#     def get_items_within_radius(lat, lng, radius):
#         """Return all sample locations within a given radius (in meters)"""
#
#         #TODO: The arbitrary limit = 100 is just a quick way to make sure
#         # we won't return tons of entries at once,
#         # paging needs to be in place for real usecase
#         results = SampleLocation.query.filter(
#             ST_DWithin(
#                 cast(SampleLocation.geom, Geography),
#                 cast(from_shape(Point(lng, lat)), Geography),
#                 radius)
#             ).limit(100).all()
#
#         return [l.to_dict() for l in results]
#
#     def get_location_latitude(self):
#         point = to_shape(self.geom)
#         return point.y
#
#     def get_location_longitude(self):
#         point = to_shape(self.geom)
#         return point.x
#
#     def to_dict(self):
#         return {
#             'id': self.id,
#             'description': self.description,
#             'location': {
#                 'lng': self.get_location_longitude(),
#                 'lat': self.get_location_latitude()
#             }
#         }
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