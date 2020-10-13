import flask_sqlalchemy
from app import db


class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_message = db.Column(db.String(500))
    
    def __init__(self, a):
        self.chat_message = a
        
    def __repr__(self):
        return '<Chat message: %s>' % self.chat_message 
