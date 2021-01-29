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
        exit('ERROR: token.json not found. Please run auth.py')
    except json.decoder.JSONDecodeError:
        exit('ERROR: token.json could not be parsed')
    return token['access_token']

def getRefreshToken():
    try:
        with open(os.path.dirname(os.path.realpath(__file__))+'/token.json', 'r') as file:
            token = json.load(file)
    except FileNotFoundError:
        exit('ERROR: token.json not found')
    try:
        return token['refresh_token']
    except KeyError:
        exit('ERROR: refresh_token not available')