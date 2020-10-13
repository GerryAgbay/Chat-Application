# app.py
from os.path import join, dirname
from dotenv import load_dotenv
import os
import flask
import flask_sqlalchemy
import flask_socketio
import models 
from flask import request
import json
import requests

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
    all_messages = [ \
        db_address.address for db_address in \
        db.session.query(models.Usps).all()]
        
    socketio.emit(channel, { 'allMessages': all_messages })
    
count = 0

@socketio.on('connect')
def on_connect():
    print('Someone connected!')
    
    global count
    count += 1
    
    socketio.emit('status', {'count': count})
    socketio.emit('connected', { 'test': 'Connected'})
    
    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)
    

@socketio.on('disconnect')
def on_disconnect():
    print ('Someone disconnected!')
    
    global count
    count -= 1
    socketio.emit('status', {'count': count})
    

@socketio.on('new message input')
def on_new_address(data):
    print("Got an event for new message input with data:", data)
    
    db.session.add(models.Usps(request.sid + ": " + data["message"]));
    db.session.commit();
    
    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)
    BotParse(data)
    
def BotParse(data):
    #print(data)
    inputString = data["message"]
    #print(inputString[16:])
    inputList = inputString.split(" ")

    botName = "Bot"
    
    if (inputList[0] == "!!"):
        if (inputList[1] == "about") or (inputList[1] == "ABOUT"):
            botMsg = "My name is Bot. I am a chat bot that has different functionalities. Enter '!! help' to get a list of my commands."
            db.session.add(models.Usps(botName.upper() + ": " + botMsg.upper()));
            db.session.commit();
            emit_all_messages(MESSAGES_RECEIVED_CHANNEL)
        
        elif (inputList[1] == "help") or (inputList[1] == "HELP"):
            botMsg = "Here is a list of my commands: [!! about, !! help, !! funtranslate <message>]"
            db.session.add(models.Usps(botName.upper() + ": " + botMsg.upper()));
            db.session.commit();
            emit_all_messages(MESSAGES_RECEIVED_CHANNEL)
            
        elif (inputList[1] == "funtranslate") or (inputList[1] == "FUNTRANSLATE"):
            translate_url = "https://api.funtranslations.com/translate/dothraki.json?text=" + inputString[16:]
            translate_response = requests.request("GET", translate_url)
            translate_dictionary = translate_response.json()
            #print(translate_dictionary)
            
            if (translate_dictionary["error"]):
                error_msg = translate_dictionary["error"]["message"]
                botMsg = error_msg
                db.session.add(models.Usps(botName.upper() + ": " + botMsg.upper()));
                db.session.commit();
                emit_all_messages(MESSAGES_RECEIVED_CHANNEL)
                
            else:
                translate_contents = translate_dictionary["contents"]
                translated = translate_contents["translated"]
            
                botMsg = "Dothraki Translation: " + translated
                db.session.add(models.Usps(botName.upper() + ": " + botMsg.upper()));
                db.session.commit();
                emit_all_messages(MESSAGES_RECEIVED_CHANNEL)
            
        else:
            botMsg = "Sorry, I don't recognize that command. Enter '!! help' to get a list of my commands."
            db.session.add(models.Usps(botName.upper() + ": " + botMsg.upper()));
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
