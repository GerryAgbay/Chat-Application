from os.path import dirname, join
import sys

sys.path.append(join(dirname(__file__), "../"))
from chatBot import bot
import chatBot
import unittest

KEY_INPUT = "input_message"
KEY_EXPECTED = "expected"
KEY_BOT_MSG = "return_key"


class BotTestEmpty(unittest.TestCase):
    def setUp(self):
        self.success_test_params = [
            {
                KEY_INPUT: {"message": "!!"},
                KEY_EXPECTED: {
                    KEY_BOT_MSG: "I'm smart but I don't know everything. Enter '!! help' and try again with something I actually understand."
                },
            }
        ]

    def testBotEmptySuccess(self):
        for test in self.success_test_params:
            response = bot(test[KEY_INPUT])
            expected = test[KEY_EXPECTED]

        self.assertEqual(response, expected[KEY_BOT_MSG])


# -------


class BotTestAbout(unittest.TestCase):
    def setUp(self):
        self.success_test_params = [
            {
                KEY_INPUT: {"message": "!! about"},
                KEY_EXPECTED: {
                    KEY_BOT_MSG: (
                        "I'm the Halfbot. I may be stuck here but you know what? If you're going to be a cripple, it's better to be a rich cripple. "
                        + "A mind needs books and everything's better with some wine in the belly. That's what I do: I drink and I know things. "
                        + "If you want to know what you can ask from me, enter '!! help'. I can't make any promises though."
                    )
                },
            }
        ]

    def testBotAboutSuccess(self):
        for test in self.success_test_params:
            response = bot(test[KEY_INPUT])
            expected = test[KEY_EXPECTED]

        self.assertEqual(response, expected[KEY_BOT_MSG])


# -------


class BotTestHelp(unittest.TestCase):
    def setUp(self):
        self.success_test_params = [
            {
                KEY_INPUT: {"message": "!! help"},
                KEY_EXPECTED: {
                    KEY_BOT_MSG: "Here's a list of what I know: [!! about, !! help, !! funtranslate <message>, !! randjoke, !! randint [min int] [max int]]"
                },
            }
        ]

    def testBotHelpSuccess(self):
        for test in self.success_test_params:
            response = bot(test[KEY_INPUT])
            expected = test[KEY_EXPECTED]

        self.assertEqual(response, expected[KEY_BOT_MSG])


# -------


class BotTestWrong(unittest.TestCase):
    def setUp(self):
        self.success_test_params = [
            {
                KEY_INPUT: {"message": "!! non-existent"},
                KEY_EXPECTED: {
                    KEY_BOT_MSG: "I'm smart but I don't know everything. Enter '!! help' and try again with something I actually understand."
                },
            }
        ]

    def testBotWrongSuccess(self):
        for test in self.success_test_params:
            response = bot(test[KEY_INPUT])
            expected = test[KEY_EXPECTED]

        self.assertEqual(response, expected[KEY_BOT_MSG])


# -------


class Bot_Test_Empty_Fail(unittest.TestCase):
    def setUp(self):
        self.fail_test_params = [
            {
                KEY_INPUT: {"message": "!!"},
                KEY_EXPECTED: {
                    KEY_BOT_MSG: "I'm not smart but I don't know everything. Enter '!! help' and try again with something I actually understand."
                },
            }
        ]

    def test_bot_empty_fail(self):
        for test in self.fail_test_params:
            response = bot(test[KEY_INPUT])
            expected = test[KEY_EXPECTED]

        self.assertNotEqual(response, expected[KEY_BOT_MSG])


# -------


class Bot_Test_About_Fail(unittest.TestCase):
    def setUp(self):
        self.fail_test_params = [
            {
                KEY_INPUT: {"message": "!! about"},
                KEY_EXPECTED: {
                    KEY_BOT_MSG: (
                        "I'm not the Halfbot. I may be stuck here but you know what? If you're going to be a cripple, it's better to be a rich cripple. "
                        + "A mind needs books and everything's better with some wine in the belly. That's what I do: I drink and I know things. "
                        + "If you want to know what you can ask from me, enter '!! help'. I can't make any promises though."
                    )
                },
            }
        ]

    def test_bot_about_fail(self):
        for test in self.fail_test_params:
            response = bot(test[KEY_INPUT])
            expected = test[KEY_EXPECTED]

        self.assertNotEqual(response, expected[KEY_BOT_MSG])


# -------


class Bot_Test_Help_Fail(unittest.TestCase):
    def setUp(self):
        self.fail_test_params = [
            {
                KEY_INPUT: {"message": "!! help"},
                KEY_EXPECTED: {
                    KEY_BOT_MSG: "Here's not a list of what I know: [!! about, !! help, !! funtranslate <message>, !! randjoke, !! randint <min> <max>]"
                },
            }
        ]

    def test_bot_help_fail(self):
        for test in self.fail_test_params:
            response = bot(test[KEY_INPUT])
            expected = test[KEY_EXPECTED]

        self.assertNotEqual(response, expected[KEY_BOT_MSG])


# -------


class Bot_Test_Wrong_Fail(unittest.TestCase):
    def setUp(self):
        self.fail_test_params = [
            {
                KEY_INPUT: {"message": "!! unknown"},
                KEY_EXPECTED: {
                    KEY_BOT_MSG: "Not this: I'm smart but I don't know everything. Enter '!! help' and try again with something I actually understand."
                },
            }
        ]

    def test_bot_wrong_fail(self):
        for test in self.fail_test_params:
            response = bot(test[KEY_INPUT])
            expected = test[KEY_EXPECTED]

        self.assertNotEqual(response, expected[KEY_BOT_MSG])


# -------


class Bot_Test_Randint1(unittest.TestCase):
    def setUp(self):
        self.success_test_params = [
            {
                KEY_INPUT: {"message": "!! randint 1 2 3 4"},
                KEY_EXPECTED: {
                    KEY_BOT_MSG: "Enter two integers like so: !! randint [min int] [max int]"
                },
            }
        ]

    def test_bot_randint1_success(self):
        for test in self.success_test_params:
            response = bot(test[KEY_INPUT])
            expected = test[KEY_EXPECTED]

        self.assertEqual(response, expected[KEY_BOT_MSG])


# -------


class Bot_Test_Randint2(unittest.TestCase):
    def setUp(self):
        self.success_test_params = [
            {
                KEY_INPUT: {"message": "!! randint hello 10"},
                KEY_EXPECTED: {
                    KEY_BOT_MSG: "You didn't enter an integer. Ask by doing: !! randint [min int] [max int]"
                },
            }
        ]

    def test_bot_randint2_success(self):
        for test in self.success_test_params:
            response = bot(test[KEY_INPUT])
            expected = test[KEY_EXPECTED]

        self.assertEqual(response, expected[KEY_BOT_MSG])


# -------


class Bot_Test_Randint1_Fail(unittest.TestCase):
    def setUp(self):
        self.fail_test_params = [
            {
                KEY_INPUT: {"message": "!! randint 5 10"},
                KEY_EXPECTED: {
                    KEY_BOT_MSG: "Enter two integers like so: !! randint [min int] [max int]"
                },
            }
        ]

    def test_bot_randint1_fail(self):
        for test in self.fail_test_params:
            response = bot(test[KEY_INPUT])
            expected = test[KEY_EXPECTED]

        self.assertNotEqual(response, expected[KEY_BOT_MSG])


# -------


class Bot_Test_Randint2_Fail(unittest.TestCase):
    def setUp(self):
        self.fail_test_params = [
            {
                KEY_INPUT: {"message": "!! randint 10 20"},
                KEY_EXPECTED: {
                    KEY_BOT_MSG: "You didn't enter an integer. Ask by doing: !! randint [min int] [max int]"
                },
            }
        ]

    def test_bot_randint2_fail(self):
        for test in self.fail_test_params:
            response = bot(test[KEY_INPUT])
            expected = test[KEY_EXPECTED]

        self.assertNotEqual(response, expected[KEY_BOT_MSG])


if __name__ == "__main__":
    unittest.main()
