import os
from datetime import datetime
from flask_login import UserMixin, LoginManager, current_user
#from app import db, app
from werkzeug.security import generate_password_hash
import base64
from Crypto.Protocol.KDF import scrypt
from Crypto.Random import get_random_bytes
from cryptography.fernet import Fernet
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_sqlalchemy import SQLAlchemy
from config import DevConfig

from flask import render_template

db = SQLAlchemy()


def encrypt(data, key):
    return Fernet(key).encrypt(bytes(data, 'utf-8'))


def decrypt(data, key):
    return Fernet(key).decrypt(data).decode("utf-8")

class Sea_Level_Rise(db.Model):
    __tablename__ = 'sea_level_rise'

    id = db.Column(db.Integer, primary_key=True)
    entity = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(100), nullable=True)
    day = db.Column(db.String(100), nullable=False)
    sea_level_rise_average = db.Column(db.Float, nullable=True)

    def __init__(self, entity, code, day, sea_level_rise_average):
        self.entity = entity
        self.code = code
        self.day = day
        self.sea_level_rise_average = sea_level_rise_average

class Temp_Anomaly(db.Model):
    __tablename__ = 'temperature_anomaly'

    id = db.Column(db.Integer, primary_key=True)
    Entity = db.Column(db.String(100), nullable=False)
    Code = db.Column(db.String(100), nullable=True)
    Day = db.Column(db.String(100), nullable=False)
    Temperature_Anomaly = db.Column(db.Float, nullable=False)

    def __init__(self, Entity, Code, Day, Temperature_Anomaly):
        self.Entity = Entity
        self.Code = Code
        self.Day = Day
        self.Temperature_Anomaly = Temperature_Anomaly

class C02_Concentration(db.Model):
    __tablename__ = 'co2_concentration'

    id = db.Column(db.Integer, primary_key=True)
    entity = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(100), nullable=True)
    day = db.Column(db.String, nullable=False)
    average_co2_concentrations = db.Column(db.Float, nullable=True)
    trend_co2_concentrations = db.Column(db.Float, nullable=True)

    def __init__(self, entity, code, day, average_co2_concentrations, trend_co2_concentrations):
        self.entity = entity
        self.code = code
        self.day = day
        self.average_co2_concentrations = average_co2_concentrations
        self.trend_co2_concentrations = trend_co2_concentrations


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    # User authentication information.
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    pin_key = db.Column(db.String(100), nullable=False)

    # User activity information
    registered_on = db.Column(db.DateTime, nullable=False)
    last_logged_in = db.Column(db.DateTime, nullable=True)
    current_logged_in = db.Column(db.DateTime, nullable=True)

    # User information
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False, default='user')

    # crypto key for user
    encrypt_key = db.Column(db.BLOB)

    # relationship between user and comments tables
    comments = db.relationship('Comments', cascade='all,delete-orphan', backref='users')

    def get_reset_token(self, expires_seconds=600):
        # initialise serializer
        s = Serializer(DevConfig.SECRET_KEY, expires_seconds)
        # create serializer payload
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(DevConfig.SECRET_KEY)
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __init__(self, email, firstname, lastname, phone, password, pin_key, role):
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.phone = phone
        self.password = generate_password_hash(password)
        self.pin_key = pin_key
        self.encrypt_key = base64.urlsafe_b64encode(
            scrypt(password, str(get_random_bytes(32)), 32, N=2 ** 14, r=8, p=1))
        self.role = role
        self.registered_on = datetime.now()
        self.last_logged_in = None
        self.current_logged_in = None


class Forum(db.Model):
    __tablename__ = 'forum'

    post_id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, nullable=False)
    title = db.Column(db.Text, nullable=False, default=False)
    body = db.Column(db.Text, nullable=False, default=False)

    # relationship with comments table
    comments = db.relationship('Comments', cascade="all,delete-orphan", backref='forum')

    def __init__(self, user_id, title, body):
        self.user_id = user_id
        self.created = datetime.now()
        self.title = title
        self.body = body


class Comments(db.Model):
    __tablename__ = 'comments'

    comment_id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    post_id = db.Column(db.Integer, db.ForeignKey(Forum.post_id))

    def __init__(self, body, user_id, post_id):
        self.body = body
        self.timestamp = datetime.now()
        self.user_id = user_id
        self.post_id = post_id

def db_empty():
    try:
        db_size = os.stat("climate-action.db").st_size
        if db_size > 100:
            return False
        else:
            return True
    except:
        return True


def init_db():
    db.drop_all()
    db.create_all()
    admin = User(email='admin@email.com',
                 password='Admin1!',
                 pin_key='BFB5S34STBLZCOB22K6PPYDCMZMH46OJ',
                 firstname='Alice',
                 lastname='Jones',
                 phone='0191-123-4567',
                 role='admin')

    db.session.add(admin)
    db.session.commit()
