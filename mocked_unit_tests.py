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
            
class BotTestFuntranslate(unittest.TestCase):
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
        
        
            
if __name__ == '__main__':
    unittest.main()