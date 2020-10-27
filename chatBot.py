#import app
from app import models
import requests
import random
from flask import request

    
def bot(data):
    inputString = data["message"]
    inputList = inputString.split(" ")
    
    if (inputList[0] == "!!"):
        if (len(inputList) == 1):
            botMsg = "I'm smart but I don't know everything. Enter '!! help' and try again with something I actually understand."
            return botMsg
            
        if (inputList[1] == "about") or (inputList[1] == "ABOUT") or (inputList[1] == "About"):
            botMsg = ("I'm the Halfbot. I may be stuck here but you know what? If you're going to be a cripple, it's better to be a rich cripple. " + 
            "A mind needs books and everything's better with some wine in the belly. That's what I do: I drink and I know things. " + 
            "If you want to know what you can ask from me, enter '!! help'. I can't make any promises though.")
            return botMsg
        
        elif (inputList[1] == "help") or (inputList[1] == "HELP") or (inputList[1] == "Help"):
            botMsg = "Here's a list of what I know: [!! about, !! help, !! funtranslate <message>, !! randjoke, !! randint <min> <max>]"
            return botMsg
            
        elif (inputList[1] == "funtranslate") or (inputList[1] == "FUNTRANSLATE") or (inputList[1] == "Funtranslate"):
            translate_url = "https://api.funtranslations.com/translate/dothraki.json?text=" + inputString[16:]
            translate_response = requests.get(translate_url)
            translate_dictionary = translate_response.json()
                
            if ("contents" in translate_dictionary.keys()):
                translate_contents = translate_dictionary["contents"]
                translated = translate_contents["translated"]
                botMsg = "In Dothraki: " + translated
                return botMsg
                
            elif ("error" in translate_dictionary.keys()):
                error_msg = translate_dictionary["error"]["message"]
                botMsg = "This is what my sources say: " + error_msg
                return botMsg
                
        elif (inputList[1] == "randint") or (inputList[1] == "RANDINT") or (inputList[1] == "Randint") and isinstance(int(inputList[2]), int) and isinstance(int(inputList[3]), int):
            integer = random.randint(int(inputList[2]), int(inputList[3]))
            botMsg = "Here's a random integer: " + str(integer)
            return botMsg
            
        elif (inputList[1] == "randjoke") or (inputList[1] == "RANDJOKE") or (inputList[1] == "Randjoke"):
            joke_url = "https://sv443.net/jokeapi/v2/joke/Any?"
            joke_response = requests.get(joke_url)
            joke_dictionary = joke_response.json()
            
            if ("joke" in joke_dictionary.keys()):
                joke_contents = joke_dictionary["joke"]
                botMsg = joke_contents
                return botMsg
                
            elif ("setup" in joke_dictionary.keys()):
                joke_setup = joke_dictionary["setup"] + " " + joke_dictionary["delivery"]
                botMsg = joke_setup
                return botMsg
            
        else:
            botMsg = "I'm smart but I don't know everything. Enter '!! help' and try again with something I actually understand."
            return botMsg