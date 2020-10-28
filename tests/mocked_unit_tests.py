from os.path import dirname, join
import sys

sys.path.append(join(dirname(__file__), "../"))
from chatBot import bot
import chatBot
import unittest
import app
from app import push_new_user_to_db
import unittest
import unittest.mock as mock
from unittest.mock import patch
import requests
import models


KEY_INPUT = "input_message"
KEY_EXPECTED = "expected"
KEY_BOT_MSG = "return_key"
KEY_URL = "url"
EMIT_KEY = "emit"
EMIT_DATA = "data"


class BotTestRandInt(unittest.TestCase):
    def setUp(self):
        self.success_test_params = [
            {
                KEY_INPUT: {"message": "!! randint 1 10"},
                KEY_EXPECTED: {KEY_BOT_MSG: "Here's a random integer: 5"},
            },
        ]

    def mocked_randint(self, first, second):
        return 5

    def testBotRandIntSuccess(self):
        test1 = self.success_test_params[0]
        with mock.patch("random.randint", self.mocked_randint):
            response = bot(test1[KEY_INPUT])
        expected = test1[KEY_EXPECTED]
        self.assertEqual(response, expected[KEY_BOT_MSG])


class MockedGetResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


class BotTestFuntranslate1(unittest.TestCase):
    def setUp(self):
        self.success_test_params = [
            {
                KEY_INPUT: {"message": "!! funtranslate hello my name is"},
                KEY_EXPECTED: {KEY_BOT_MSG: "In Dothraki: Hello tih hake is"},
            }
        ]

    def mocked_request(self, url):
        return MockedGetResponse(
            {
                "success": {"total": 1},
                "contents": {
                    "translated": "Hello tih hake is",
                    "text": "hello my name is",
                    "translation": "dothraki",
                },
            },
            200,
        )

    def testBotFuntranslateSuccess(self):
        test1 = self.success_test_params[0]
        with mock.patch("requests.get", self.mocked_request):
            response = bot(test1[KEY_INPUT])
        expected = test1[KEY_EXPECTED]
        self.assertEqual(response, expected[KEY_BOT_MSG])


class BotTestFuntranslate2(unittest.TestCase):
    def setUp(self):
        self.success_test_params = [
            {
                KEY_INPUT: {"message": "!! funtranslate reached limit"},
                KEY_EXPECTED: {
                    KEY_BOT_MSG: "This is what my sources say: Too Many Requests: Rate limit of 5 requests per hour exceeded. Please wait for 6 minutes and 24 seconds."
                },
            }
        ]

    def mocked_request(self, url):
        return MockedGetResponse(
            {
                "error": {
                    "code": 429,
                    "message": "Too Many Requests: Rate limit of 5 requests per hour exceeded. Please wait for 6 minutes and 24 seconds.",
                }
            },
            429,
        )

    def testBotFuntranslateSuccess(self):
        test1 = self.success_test_params[0]
        with mock.patch("requests.get", self.mocked_request):
            response = bot(test1[KEY_INPUT])
        expected = test1[KEY_EXPECTED]
        self.assertEqual(response, expected[KEY_BOT_MSG])


class BotTestRandjoke1(unittest.TestCase):
    def setUp(self):
        self.success_test_params = [
            {
                KEY_INPUT: {"message": "!! randjoke"},
                KEY_EXPECTED: {
                    KEY_BOT_MSG: "A web developer walks into a restaurant. He immediately leaves in disgust as the restaurant was laid out in tables."
                },
            }
        ]

    def mocked_request(self, url):
        return MockedGetResponse(
            {
                "error": False,
                "category": "Programming",
                "type": "twopart",
                "setup": "A web developer walks into a restaurant.",
                "delivery": "He immediately leaves in disgust as the restaurant was laid out in tables.",
                "flags": {
                    "nsfw": False,
                    "religious": False,
                    "political": False,
                    "racist": False,
                    "sexist": False,
                },
                "id": 6,
                "lang": "en",
            },
            200,
        )

    def testBotRandjokeSuccess(self):
        test1 = self.success_test_params[0]
        with mock.patch("requests.get", self.mocked_request):
            response = bot(test1[KEY_INPUT])
        expected = test1[KEY_EXPECTED]
        self.assertEqual(response, expected[KEY_BOT_MSG])


class BotTestRandjoke2(unittest.TestCase):
    def setUp(self):
        self.success_test_params = [
            {
                KEY_INPUT: {"message": "!! randjoke"},
                KEY_EXPECTED: {
                    KEY_BOT_MSG: "I've got a really good UDP joke to tell you but I don’t know if you'll get it."
                },
            }
        ]

    def mocked_request(self, url):
        return MockedGetResponse(
            {
                "error": False,
                "category": "Programming",
                "type": "single",
                "joke": "I've got a really good UDP joke to tell you but I don’t know if you'll get it.",
                "flags": {
                    "nsfw": False,
                    "religious": False,
                    "political": False,
                    "racist": False,
                    "sexist": False,
                },
                "id": 0,
                "lang": "en",
            },
            200,
        )

    def testBotRandjokeSuccess(self):
        test1 = self.success_test_params[0]
        with mock.patch("requests.get", self.mocked_request):
            response = bot(test1[KEY_INPUT])
        expected = test1[KEY_EXPECTED]
        self.assertEqual(response, expected[KEY_BOT_MSG])


class Mocked_socket_emit:
    def __init__(self, emit_key, emit_value):
        self.emit_key = emit_key["key"]
        self.emit_value = emit_value["value"]

    def json(self):
        print(self.emit_key)
        return self.emit_key


class Test_On_Connect(unittest.TestCase):
    def setUp(self):
        self.success_test_params = [
            {KEY_INPUT: 3, KEY_EXPECTED: {EMIT_KEY: "status", EMIT_DATA: {"count": 3}}}
        ]

    def mocked_socket(self, key, value):
        return ({"key": "status"}, {"value": {"count": 3}})

    def test_socket_on_connect(self):
        with mock.patch("app.socketio.emit", self.mocked_socket):
            response = app.on_connect()

        self.assertEqual(response, None)


class Mocked_Push:
    def __init__(self, name, auth, email, sid):
        self.name = name
        self.auth = auth
        self.email = email
        self.sid = sid

    def json(self):
        return self.name


class Test_Push(unittest.TestCase):
    def setUp(self):
        self.success_test_params = [
            {
                KEY_INPUT: {
                    "name": "Gerry",
                    "auth_type": "Google",
                    "email": "gerryagbayjr@gmail.com",
                    "sid": "12345",
                },
                KEY_EXPECTED: {
                    EMIT_KEY: None,
                },
            }
        ]

    def mocked_add(self, name):
        return Mocked_Push("Gerry", "Google", "gerryagbayjr@gmail.com", "12345")

    def test_push_user(self):
        test = self.success_test_params[0]
        with mock.patch("app.db.session.add", self.mocked_add):
            response = app.push_new_user_to_db(
                test[KEY_INPUT]["name"],
                models.AuthUserType.GOOGLE,
                test[KEY_INPUT]["email"],
                test[KEY_INPUT]["sid"],
            )
        expected = test[KEY_EXPECTED]
        self.assertEqual(response, expected[EMIT_KEY])


class Test_On_New_Google_User(unittest.TestCase):
    def setUp(self):
        self.success_test_params = [
            {
                KEY_INPUT: {"name": "Gerry", "email": "gerryagbayjr@gmail.com"},
                KEY_EXPECTED: {
                    EMIT_KEY: "status",
                },
            }
        ]

    def mocked_socket(self, key, value):
        return None

    def test_on_new_google_user(self):
        test = self.success_test_params[0]
        with mock.patch("app.socketio.emit", self.mocked_socket):
            response = app.on_new_google_user(test[KEY_INPUT])

        self.assertEqual(response, None)


class Mocked_Push_2:
    def __init__(self, name, sid):
        self.name = name
        self.sid = sid

    def json(self):
        return self.name


class Test_Find_Url(unittest.TestCase):
    def setUp(self):
        self.success_test_params = [
            {
                KEY_INPUT: {
                    "link": "https://smalltotall.info/wp-content/uploads/2017/04/google-favicon-vector-400x400.png",
                    "sid": "12345",
                },
                KEY_EXPECTED: {EMIT_KEY: None},
            }
        ]

    def mocked_add_2(self, link):
        return Mocked_Push_2(
            "https://smalltotall.info/wp-content/uploads/2017/04/google-favicon-vector-400x400.png",
            "12345",
        )

    def test_push_user(self):
        test = self.success_test_params[0]
        with mock.patch("app.db.session.add", self.mocked_add_2):
            response = app.find_url(test[KEY_INPUT]["link"], test[KEY_INPUT]["sid"])
        expected = test[KEY_EXPECTED]
        self.assertEqual(response, expected[EMIT_KEY])


class Test_On_Disconnect(unittest.TestCase):
    def setUp(self):
        self.success_test_params = [
            {KEY_INPUT: 1, KEY_EXPECTED: {EMIT_KEY: "status", EMIT_DATA: {"count": 1}}}
        ]

    def mocked_socket(self, key, value):
        return ({"key": "status"}, {"value": {"count": 3}})

    def test_socket_on_connect(self):
        with mock.patch("app.socketio.emit", self.mocked_socket):
            response = app.on_disconnect()

        self.assertEqual(response, None)


class Mocked_Push_3:
    def __init__(self, name):
        self.name = name

    def json(self):
        return self.name


class Test_On_New_Message_2(unittest.TestCase):
    def setUp(self):
        self.success_test_params = [
            {
                KEY_INPUT: {
                    "name": "Gerry",
                    "message": "This is a new message",
                },
                KEY_EXPECTED: {
                    EMIT_KEY: None,
                },
            }
        ]

    def mocked_add(self, name):
        return Mocked_Push_3(name)

    def test_push_user(self):
        test = self.success_test_params[0]
        with mock.patch("app.db.session.add", self.mocked_add):
            response = app.on_new_message_2(
                test[KEY_INPUT],
                ["user1", "user2", "user3"],
                "123456",
            )
        expected = test[KEY_EXPECTED]
        self.assertEqual(response, expected[EMIT_KEY])


class Mocked_Push_4:
    def __init__(self, name):
        self.name = name

    def json(self):
        return self.name


class Test_On_New_Message_(unittest.TestCase):
    def setUp(self):
        self.success_test_params = [
            {
                KEY_INPUT: {
                    "name": "Gerry",
                    "message": "!! help",
                },
                KEY_EXPECTED: {
                    EMIT_KEY: None,
                },
            }
        ]

    def mocked_add(self, name):
        return Mocked_Push_4(name)

    def test_push_user(self):
        test = self.success_test_params[0]
        with mock.patch("app.db.session.add", self.mocked_add):
            response = app.on_new_message_3(
                test[KEY_INPUT],
                "123456",
            )
        expected = test[KEY_EXPECTED]
        self.assertEqual(response, expected[EMIT_KEY])


if __name__ == "__main__":
    unittest.main()
