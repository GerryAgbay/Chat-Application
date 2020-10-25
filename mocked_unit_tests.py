import sys
#sys.path.append('../')
#import chatBot
from chatBot import bot
import chatBot
#import bot
#from bot import inputString
import unittest
import unittest.mock as mock

KEY_INPUT = "input_message"
KEY_EXPECTED = "expected"
KEY_BOT_MSG = "return_key"

class BotTestCase(unittest.TestCase):
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
        
    def testBotSuccess(self):
        test1 = self.success_test_params[0]
        with mock.patch('random.randint', self.mocked_randint):
            response = bot(test1[KEY_INPUT])
        expected = test1[KEY_EXPECTED]
        self.assertEqual(response, expected[KEY_BOT_MSG])
        
        
            
if __name__ == '__main__':
    unittest.main()