from . import db
from flask_login import UserMixin
from datetime import datetime


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    name = db.Column(db.String(150))
    password = db.Column(db.String(150))
    tasks = db.relationship('Task', backref='user', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_login = db.Column(db.DateTime, default=datetime.utcnow)
    here_since = db.Column(db.DateTime, default=datetime.utcnow)

    def to_json(self):
        json_user = {
            'id': self.id,
            'username': self.name,
            'last_login': self.last_login,
            'about_me': self.about_me
        }
        return json_user


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Integer, index=True)
    desc = db.Column(db.String(128))
    user_id = db.Column(db.Integer
                        , db.ForeignKey('user.id'))
    complete = db.Column(db.Boolean, default=False)
