# app.py
from os.path import join, dirname
from dotenv import load_dotenv
import os
import flask
import flask_sqlalchemy
import flask_socketio
import models 
from flask import request

MESSAGES_RECEIVED_CHANNEL = 'messages received'

app = flask.Flask(__name__)

socketio = flask_socketio.SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

dotenv_path = join(dirname(__file__), 'sql.env')
load_dotenv(dotenv_path)

sql_user = os.environ['SQL_USER']
sql_pwd = os.environ['SQL_PASSWORD']
dbuser = os.environ['USER']

database_uri = 'postgresql://{}:{}@localhost/postgres'.format(
    sql_user, sql_pwd)

app.config['SQLALCHEMY_DATABASE_URI'] = database_uri

db = flask_sqlalchemy.SQLAlchemy(app)
db.init_app(app)
db.app = app


db.create_all()
db.session.commit()

def emit_all_messages(channel):
    all_addresses = [ \
        db_address.address for db_address in \
        db.session.query(models.Usps).all()]
        
    socketio.emit(channel, {
        'allAddresses': all_addresses
    })
    
count = 0

@socketio.on('connect')
def on_connect():
    print('Someone connected!')
    
    global count
    count += 1
    
    socketio.emit('status', {'count': count}, broadcast=True)
    socketio.emit('connected', { 'test': 'Connected'})
    
    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)
    

@socketio.on('disconnect')
def on_disconnect():
    print ('Someone disconnected!')
    

@socketio.on('new message input')
def on_new_address(data):
    print("Got an event for new message input with data:", data)
    
    db.session.add(models.Usps(request.sid + ": " + data["message"]));
    db.session.commit();
    
    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)

@app.route('/')
def index():
    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)

    return flask.render_template("index.html")

if __name__ == '__main__': 
    socketio.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=True
    )
