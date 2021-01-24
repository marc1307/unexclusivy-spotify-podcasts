import os, json

def readCfg():
    try:
        with open(os.path.dirname(os.path.realpath(__file__))+'/config.json', 'r') as file:
            config = json.load(file)
    except FileNotFoundError:
        exit('ERROR: config.json not found')
    return config

def readToken():
    try:
        with open(os.path.dirname(os.path.realpath(__file__))+'/token.json', 'r') as file:
            token = json.load(file)
    except FileNotFoundError:
        exit('ERROR: token.json not found')
    return token['token']

def debug():
    return True