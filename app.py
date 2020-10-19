from os.path import join, dirname
from dotenv import load_dotenv
import os
import flask
import flask_sqlalchemy
import flask_socketio
import models 
from flask import request
from chatBot import bot


MESSAGES_RECEIVED_CHANNEL = 'messages received'

app = flask.Flask(__name__)

socketio = flask_socketio.SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

dotenv_path = join(dirname(__file__), 'sql.env')
load_dotenv(dotenv_path)

database_uri = os.environ['DATABASE_URL'] 

app.config['SQLALCHEMY_DATABASE_URI'] = database_uri

db = flask_sqlalchemy.SQLAlchemy(app)
db.init_app(app)
db.app = app


db.create_all()
db.session.commit()


def emit_all_messages(channel):
    all_messages = [ \
        db_message.chat_message for db_message in \
        db.session.query(models.Chat).all()]
        
    socketio.emit(channel, { 'allMessages': all_messages })
    
    
def push_new_user_to_db(name, auth_type, email, sid):
    # TODO remove this check after the logic works correctly
    if name != "John Doe":
        db.session.add(models.AuthUser(name, auth_type, email, sid));
        db.session.commit();


@socketio.on('connect')
def on_connect():
    print('Someone connected!')
    
    socketio.emit('status', {'count': count})
    socketio.emit('connected', { 'test': 'Connected'})
    
    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)
    
    
count = 0    

@socketio.on('new google user')
def on_new_google_user(data):
    print("Got an event for new google user input with data:", data)
    push_new_user_to_db(data['name'], models.AuthUserType.GOOGLE, data['email'], request.sid)
    
    global count
    count += 1
    
    socketio.emit('status', {'count': count})
    
    
@socketio.on('disconnect')
def on_disconnect():
    print ('Someone disconnected!')
    
    global count
    if count > 0:
        count -= 1
    else:
        count == 0
        
    socketio.emit('status', {'count': count})
    

@socketio.on('new message input')
def on_new_address(data):
    print("Got an event for new message input with data:", data)
    user = [ \
        db_user.name for db_user in \
        db.session.query(models.AuthUser).filter_by(sid=request.sid)]
    db.session.add(models.Chat(user[len(user)-1] + ": " + data["message"], request.sid));
    db.session.commit();
    
    bot(data)
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