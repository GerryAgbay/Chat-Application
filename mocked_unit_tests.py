import sys
#sys.path.append('../')
#import chatBot
from chatBot import bot
import chatBot
#import bot
#from bot import inputString
import unittest
import unittest.mock as mock
import requests


KEY_INPUT = "input_message"
KEY_EXPECTED = "expected"
KEY_BOT_MSG = "return_key"

class BotTestRandInt(unittest.TestCase):
    def setUp(self):
        self.success_test_params = [
            {
                KEY_INPUT: {"message" : "!! randint 1 10"},
                KEY_EXPECTED : {
                    KEY_BOT_MSG : "Here's a random integer: 5"
                }
            },
            
            
        ]
        
    def mocked_randint(self, first, second):
        return 5
        
    def testBotRandIntSuccess(self):
        test1 = self.success_test_params[0]
        with mock.patch('random.randint', self.mocked_randint):
            response = bot(test1[KEY_INPUT])
        expected = test1[KEY_EXPECTED]
        self.assertEqual(response, expected[KEY_BOT_MSG])
        
#-------

class MockedGetResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code
            
    def json(self):
        return self.json_data
        
#-------
            
class BotTestFuntranslate1(unittest.TestCase):
    def setUp(self):
        self.success_test_params = [
            {
                KEY_INPUT: {"message" : "!! funtranslate hello my name is"},
                KEY_EXPECTED : {
                    KEY_BOT_MSG : "In Dothraki: Hello tih hake is"
                }
            }
        ]
        
    def mocked_request(self, url):
        return MockedGetResponse({'success': {'total': 1}, 'contents': {'translated': 'Hello tih hake is', 'text': 'hello my name is', 'translation': 'dothraki'}}, 200)
        
    def testBotFuntranslateSuccess(self):
        test1 = self.success_test_params[0]
        with mock.patch('requests.get', self.mocked_request):
            response = bot(test1[KEY_INPUT])
        expected = test1[KEY_EXPECTED]
        self.assertEqual(response, expected[KEY_BOT_MSG])
        
#-------
            
class BotTestFuntranslate2(unittest.TestCase):
    def setUp(self):
        self.success_test_params = [
            {
                KEY_INPUT: {"message" : "!! funtranslate reached limit"},
                KEY_EXPECTED : {
                    KEY_BOT_MSG : "This is what my sources say: Too Many Requests: Rate limit of 5 requests per hour exceeded. Please wait for 6 minutes and 24 seconds."
                }
            }
        ]
        
    def mocked_request(self, url):
        return MockedGetResponse({'error': {'code': 429, 'message': 'Too Many Requests: Rate limit of 5 requests per hour exceeded. Please wait for 6 minutes and 24 seconds.'}}, 429)
        
    def testBotFuntranslateSuccess(self):
        test1 = self.success_test_params[0]
        with mock.patch('requests.get', self.mocked_request):
            response = bot(test1[KEY_INPUT])
        expected = test1[KEY_EXPECTED]
        self.assertEqual(response, expected[KEY_BOT_MSG])
        
#-------
            
class BotTestRandjoke1(unittest.TestCase):
    def setUp(self):
        self.success_test_params = [
            {
                KEY_INPUT: {"message" : "!! randjoke"},
                KEY_EXPECTED : {
                    KEY_BOT_MSG : "A web developer walks into a restaurant. He immediately leaves in disgust as the restaurant was laid out in tables."
                }
            }
        ]
        
    def mocked_request(self, url):
        return MockedGetResponse({'error': False, 'category': 'Programming', 'type': 'twopart', 'setup': 'A web developer walks into a restaurant.', 
        'delivery': 'He immediately leaves in disgust as the restaurant was laid out in tables.', 'flags': {'nsfw': False, 'religious': False, 
        'political': False, 'racist': False, 'sexist': False}, 'id': 6, 'lang': 'en'}, 200)
        
    def testBotRandjokeSuccess(self):
        test1 = self.success_test_params[0]
        with mock.patch('requests.get', self.mocked_request):
            response = bot(test1[KEY_INPUT])
        expected = test1[KEY_EXPECTED]
        self.assertEqual(response, expected[KEY_BOT_MSG])
        
#------

class BotTestRandjoke2(unittest.TestCase):
    def setUp(self):
        self.success_test_params = [
            {
                KEY_INPUT: {"message" : "!! randjoke"},
                KEY_EXPECTED : {
                    KEY_BOT_MSG : "I've got a really good UDP joke to tell you but I don’t know if you'll get it."
                }
            }
        ]
        
    def mocked_request(self, url):
        return MockedGetResponse({'error': False, 'category': 'Programming', 'type': 'single', 'joke': "I've got a really good UDP joke to tell you but I don’t know if you'll get it.", 'flags': {'nsfw': False, 'religious': False, 'political': False, 'racist': False, 'sexist': False}, 'id': 0, 'lang': 'en'}, 200)
        
    def testBotRandjokeSuccess(self):
        test1 = self.success_test_params[0]
        with mock.patch('requests.get', self.mocked_request):
            response = bot(test1[KEY_INPUT])
        expected = test1[KEY_EXPECTED]
        self.assertEqual(response, expected[KEY_BOT_MSG])

            
if __name__ == '__main__':
    unittest.main()