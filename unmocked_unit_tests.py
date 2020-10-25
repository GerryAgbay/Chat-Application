import sys
#sys.path.append('../')
#import chatBot
from chatBot import bot
import chatBot
#import bot
#from bot import inputString
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
                    KEY_BOT_MSG : "I'm smart but I don't know everything. Enter '!! help' and try again with something I actually understand."
                }
            },
            {
                KEY_INPUT: {"message" : "!! about"},
                KEY_EXPECTED : {
                    KEY_BOT_MSG : ("I'm the Halfbot. I may be stuck here but you know what? If you're going to be a cripple, it's better to be a rich cripple. " + 
                    "A mind needs books and everything's better with some wine in the belly. That's what I do: I drink and I know things. " + 
                    "If you want to know what you can ask from me, enter '!! help'. I can't make any promises though.")
                }
            },
            {
                KEY_INPUT: {"message" : "!! help"},
                KEY_EXPECTED : {
                    KEY_BOT_MSG : "Here's a list of what I know: [!! about, !! help, !! funtranslate <message>, !! randjoke, !! randint <min> <max>]"
                }
            },
             {
                KEY_INPUT: {"message" : "!! hello"},
                KEY_EXPECTED : {
                    KEY_BOT_MSG : "I'm smart but I don't know everything. Enter '!! help' and try again with something I actually understand."
                }
            }
        ]
        
    def testBotSuccess(self):
        for test in self.success_test_params:
            response = bot(test[KEY_INPUT])
            expected = test[KEY_EXPECTED]
            
            self.assertEqual(response, expected[KEY_BOT_MSG])
            
if __name__ == '__main__':
    unittest.main()