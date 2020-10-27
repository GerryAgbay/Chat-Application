import flask_sqlalchemy
from app import db
from enum import Enum


class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_message = db.Column(db.String(500))
    sid = db.Column(db.String(120))

    def __init__(self, a, b):
        self.chat_message = a
        self.sid = b

    def __repr__(self):
        return "<Chat message: {}\nsid: {}>".format(self.chat_message, self.sid)


class AuthUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    auth_type = db.Column(db.String(120))
    name = db.Column(db.String(120))
    email = db.Column(db.String(120))
    sid = db.Column(db.String(120))

    def __init__(self, name, auth_type, email, sid):
        assert type(auth_type) is AuthUserType
        self.name = name
        self.auth_type = auth_type.value
        self.email = email
        self.sid = sid

    def __repr__(self):
        return "<User name: {}\ntype: {}\nemail: {}\nsid: {}".format(
            self.name, self.auth_type, self.email, self.sid
        )


class AuthUserType(Enum):
    GOOGLE = "google"
