from os.path import join, dirname
from dotenv import load_dotenv
import os
import flask
import flask_sqlalchemy
import flask_socketio
from flask import request
import re

MESSAGES_RECEIVED_CHANNEL = "messages received"

app = flask.Flask(__name__)

socketio = flask_socketio.SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

dotenv_path = join(dirname(__file__), "sql.env")
load_dotenv(dotenv_path)

database_uri = os.environ["DATABASE_URL"]

app.config["SQLALCHEMY_DATABASE_URI"] = database_uri

db = flask_sqlalchemy.SQLAlchemy(app)

import models


def emit_all_messages(channel):
    all_messages = [
        db_message.chat_message for db_message in db.session.query(models.Chat).all()
    ]

    socketio.emit(channel, {"allMessages": all_messages})


def push_new_user_to_db(name, auth_type, email, sid):
    db.session.add(models.AuthUser(name, auth_type, email, sid))
    db.session.commit()


def findUrl(data, sid):
    item = data
    user_sid = sid
    r_url = re.compile(r"^https?:")
    r_image = re.compile(r".*\.(jpg|png|gif)$")
    if r_url.match(item) or r_image.match(item):
        db.session.add(models.Chat(item, user_sid))
        db.session.commit()


@socketio.on("connect")
def on_connect():
    print("Someone connected!")

    socketio.emit("status", {"count": count})
    socketio.emit("connected", {"test": "Connected"})

    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)


count = 0


@socketio.on("new google user")
def on_new_google_user(data):
    print("Got an event for new google user input with data:", data)

    global count
    count += 1

    socketio.emit("status", {"count": count})


@socketio.on("new google user 2")
def on_new_google_user_2(data):
    push_new_user_to_db(
        data["name"], models.AuthUserType.GOOGLE, data["email"], request.sid
    )


@socketio.on("disconnect")
def on_disconnect():
    print("Someone disconnected!")

    global count
    if count > 0:
        count -= 1
    else:
        count = 0

    socketio.emit("status", {"count": count})


@socketio.on("new message input")
def on_new_message_helper(data):
    on_new_message(data, request.sid)
    on_new_message_3(data, request.sid)


# @socketio.on("new message input")
def on_new_message(data, rsid):
    request_sid = rsid
    print("Got an event for new message input with data:", data)
    user = [
        db_user.name
        for db_user in db.session.query(models.AuthUser).filter_by(sid=request_sid)
    ]
    on_new_message_2(data, user, request_sid)


def on_new_message_2(data, user, rsid):
    request_sid = rsid
    db.session.add(
        models.Chat(user[len(user) - 1] + ": " + data["message"], request_sid)
    )
    db.session.commit()

    findUrl(data["message"], request_sid)


def on_new_message_3(data, rsid):
    from chatBot import bot

    request_sid = rsid

    if bot(data):
        botName = "Halfbot"
        db.session.add(
            models.Chat(botName.upper() + ": " + bot(data).upper(), request_sid)
        )
        db.session.commit()

    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)


@app.route("/")
def index():
    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)

    return flask.render_template("index.html")


if __name__ == "__main__":
    socketio.run(
        app,
        host=os.getenv("IP", "0.0.0.0"),
        port=int(os.getenv("PORT", 8080)),
        debug=True,
    )
