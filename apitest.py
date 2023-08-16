import openai as ai
import os
import json
def init_config(): # Init config file
    if not os.path.exists("Config.json"):
        with open("Config.json", "w") as f:
            json.dump({ # Default config
                "model": "gpt-3.5-turbo",
                "temperature": 0.7,
                "max_tokens": 1024,
            })
    config = json.load(open("initSysPrompt.json", "r"))
    return config
def init_api_key():
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        api_key = input("API Key not detected, please enter your API Key: ")
        os.environ["OPENAI_API_KEY"] = api_key
    
    return api_key
def session_save_load(session,save_or_load):

def main_process():
    response = ai.ChatCompletion.create(
        model="davinci",
    