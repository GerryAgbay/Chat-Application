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
import random

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
    
    db.session.add(models.Chat(request.sid + ": " + data["message"]));
    db.session.commit();
    
    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)
    bot(data)
    
    
def botDB(botName, botMsg):
    db.session.add(models.Chat(botName.upper() + ": " + botMsg.upper()));
    db.session.commit();
    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)
    
    
def bot(data):
    inputString = data["message"]
    inputList = inputString.split(" ")
    botName = "Halfbot"
    
    if (inputList[0] == "!!"):
        if (len(inputList) == 1):
            botMsg = "I'm smart but I don't know everything. Enter '!! help' and try again with something I actually understand."
            botDB(botName, botMsg)
            
        if (inputList[1] == "about") or (inputList[1] == "ABOUT") or (inputList[1] == "About"):
            botMsg = ("I'm the Halfbot. I may be stuck here but you know what? If you're going to be a cripple, it's better to be a rich cripple. " + 
            "A mind needs books and everything's better with some wine in the belly. That's what I do: I drink and I know things. " + 
            "If you want to know what you can ask from me, enter '!! help'. I can't make any promises though.")
            botDB(botName, botMsg)
        
        elif (inputList[1] == "help") or (inputList[1] == "HELP") or (inputList[1] == "Help"):
            botMsg = "Here's a list of what I know: [!! about, !! help, !! funtranslate <message>, !! randjoke, !! randint <min> <max>]"
            botDB(botName, botMsg)
            
        elif (inputList[1] == "funtranslate") or (inputList[1] == "FUNTRANSLATE") or (inputList[1] == "Funtranslate"):
            translate_url = "https://api.funtranslations.com/translate/dothraki.json?text=" + inputString[16:]
            translate_response = requests.request("GET", translate_url)
            translate_dictionary = translate_response.json()
                
            if ("contents" in translate_dictionary.keys()):
                translate_contents = translate_dictionary["contents"]
                translated = translate_contents["translated"]
                botMsg = "In Dothraki: " + translated
                botDB(botName, botMsg)
                
            elif ("error" in translate_dictionary.keys()):
                error_msg = translate_dictionary["error"]["message"]
                botMsg = "This is what my sources say: " + error_msg
                botDB(botName, botMsg)
                
        elif (inputList[1] == "randint") or (inputList[1] == "RANDINT") or (inputList[1] == "Randint") and isinstance(int(inputList[2]), int) and isinstance(int(inputList[3]), int):
            integer = random.randint(int(inputList[2]), int(inputList[3]))
            botMsg = "Here's a random integer: " + str(integer)
            botDB(botName, botMsg)
            
        elif (inputList[1] == "randjoke") or (inputList[1] == "RANDJOKE") or (inputList[1] == "Randjoke"):
            joke_url = "https://sv443.net/jokeapi/v2/joke/Any?"
            joke_response = requests.request("GET", joke_url)
            joke_dictionary = joke_response.json()
            
            if ("joke" in joke_dictionary.keys()):
                joke_contents = joke_dictionary["joke"]
                botMsg = joke_contents
                botDB(botName, botMsg)
                
            elif ("setup" in joke_dictionary.keys()):
                joke_setup = joke_dictionary["setup"] + " " + joke_dictionary["delivery"]
                botMsg = joke_setup
                botDB(botName, botMsg)
            
        else:
            botMsg = "I'm smart but I don't know everything. Enter '!! help' and try again with something I actually understand."
            botDB(botName, botMsg)


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