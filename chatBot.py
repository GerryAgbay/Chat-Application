import random
import requests
from app import models
from flask import request


def bot(data):
    input_string = data["message"]
    input_list = input_string.split(" ")

    if input_list[0] == "!!":
        if len(input_list) == 1:
            bot_msg = "I'm smart but I don't know everything. Enter '!! help' and try again with something I actually understand."
            return bot_msg

        if (
            (input_list[1] == "about")
            or (input_list[1] == "ABOUT")
            or (input_list[1] == "About")
        ):
            bot_msg = (
                "I'm the Halfbot. I may be stuck here but you know what? If you're going to be a cripple, it's better to be a rich cripple. "
                + "A mind needs books and everything's better with some wine in the belly. That's what I do: I drink and I know things. "
                + "If you want to know what you can ask from me, enter '!! help'. I can't make any promises though."
            )
            return bot_msg

        elif (
            (input_list[1] == "help")
            or (input_list[1] == "HELP")
            or (input_list[1] == "Help")
        ):
            bot_msg = "Here's a list of what I know: [!! about, !! help, !! funtranslate <message>, !! randjoke, !! randint [min int] [max int]]"
            return bot_msg

        elif (
            (input_list[1] == "funtranslate")
            or (input_list[1] == "FUNTRANSLATE")
            or (input_list[1] == "Funtranslate")
        ):
            translate_url = (
                "https://api.funtranslations.com/translate/dothraki.json?text="
                + input_string[16:]
            )
            translate_response = requests.get(translate_url)
            translate_dictionary = translate_response.json()

            if "contents" in translate_dictionary.keys():
                translate_contents = translate_dictionary["contents"]
                translated = translate_contents["translated"]
                bot_msg = "In Dothraki: " + translated
                return bot_msg

            elif "error" in translate_dictionary.keys():
                error_msg = translate_dictionary["error"]["message"]
                bot_msg = "This is what my sources say: " + error_msg
                return bot_msg

        elif (
            (input_list[1] == "randint")
            or (input_list[1] == "RANDINT")
            or (input_list[1] == "Randint")
        ):
            if len(input_list) != 4:
                bot_msg = "Enter two integers like so: !! randint [min int] [max int]"
                return bot_msg

            else:
                try:
                    int(input_list[2]) and int(input_list[3])
                    integer = random.randint(int(input_list[2]), int(input_list[3]))
                    bot_msg = "Here's a random integer: " + str(integer)
                    return bot_msg

                except ValueError:
                    bot_msg = "You didn't enter an integer. Ask by doing: !! randint [min int] [max int]"
                    return bot_msg

        elif (
            (input_list[1] == "randjoke")
            or (input_list[1] == "RANDJOKE")
            or (input_list[1] == "Randjoke")
        ):
            joke_url = "https://sv443.net/jokeapi/v2/joke/Any?"
            joke_response = requests.get(joke_url)
            joke_dictionary = joke_response.json()

            if "joke" in joke_dictionary.keys():
                joke_contents = joke_dictionary["joke"]
                bot_msg = joke_contents
                return bot_msg

            elif "setup" in joke_dictionary.keys():
                joke_setup = (
                    joke_dictionary["setup"] + " " + joke_dictionary["delivery"]
                )
                bot_msg = joke_setup
                return bot_msg

        else:
            bot_msg = "I'm smart but I don't know everything. Enter '!! help' and try again with something I actually understand."
            return bot_msg
