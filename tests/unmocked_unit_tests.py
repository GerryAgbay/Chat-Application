import sys
sys.path.append('../')
import chatBot
from chatBot import bot
import unittest

KEY_INPUT = "input_message"
KEY_EXPECTED = "expected"
KEY_BOT_MSG = "return_key"

class BotTestCase(unittest.TestCase):
    def setUp(self):
        self.success_test_params = [
            {
                KEY_INPUT: {"message" : "!!"},
                KEY_EXPECTED : {
                    KEY_BOT_MSG: "I'm smart but I don't know everything. Enter '!! help' and try again with something I actually understand."
                }
            }
        ]
        
    def testBotSuccess(self):
        for test in self.success_test_params:
            response = chatBot.bot(test[KEY_INPUT])
            expected = test[KEY_EXPECTED]
            
            self.assertEqual(response, expected[KEY_BOT_MSG])
            
if __name__ == '__main__':
    unittest.main()