from app import db
from flask import g
from sqlalchemy import UniqueConstraint
from passlib.apps import custom_app_context as pwd_context
from flask_login import LoginManager, UserMixin

from datetime import datetime

from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)


SECRET_KEY = 'Some_long_text_here'
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password_hash = db.Column(db.String(128))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                            onupdate=db.func.current_timestamp())
    buckets= db.relationship('Bucketlist', backref='users', lazy='dynamic',
                            cascade="save-update, merge, delete")

    def __init__(self , username):
        self.username = username

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration = 30):
        s = Serializer(SECRET_KEY, expires_in = expiration)
        return s.dumps({ 'id': self.id })

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(SECRET_KEY)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        user = User.query.get(data['id'])
        return user


def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return (value.strftime("%Y-%m-%d") + " " + value.strftime("%H:%M:%S"))

def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id' : self.id,
            'name' : self.name,
            'date_created' : dump_datetime(self.date_created),
            'date_modified' : dump_datetime(self.date_modified),
            'created_by' : self.created_by,
            'done' : self.done
        }

class Bucketlist(db.Model):
    """This class represents the bucketlist table."""

    __tablename__ = 'bucketlists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                    onupdate=db.func.current_timestamp())
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    items = db.relationship('Item', backref='bucketlists', lazy='joined', 
                    cascade="save-update, merge, delete")
    __table_args__ = (db.UniqueConstraint('created_by', 'name', name='uix_1'),)

    def __init__(self, name, created_by):
        """initialize with name."""
        self.name = name
        self.created_by = created_by

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id' : self.id,
            'name' : self.name,
            'date_created' : dump_datetime(self.date_created),
            'date_modified' : dump_datetime(self.date_modified),
            'created_by' : self.created_by
        }

    def __repr__(self):
        return "<Bucketlist: {}>".format(self.name)

class Item(db.Model):
    """This class represents the items database table."""

    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True )
    date_created = db.Column(db.DateTime, default = db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default = db.func.current_timestamp(),
        onupdate = db.func.current_timestamp())
    done = db.Column(db.Boolean, default = False)
    bucketlist_id = db.Column(db.Integer, db.ForeignKey('bucketlists.id'))
    __table_args__ = (db.UniqueConstraint('bucketlist_id', 'name',
        name='unique_name_per_bucket'),)


    def __init__(self, name, bucketlist_id):
        self.name = name
        self.bucketlist_id = bucketlist_id
        self.done = False

    def __repr__(self):
        return "<Item: {}>".format(self.name)
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id' : self.id,
            'name' : self.name,
            'done' : self.done,
            'date_created' : dump_datetime(self.date_created),
            'date_modified' : dump_datetime(self.date_modified)
        }
