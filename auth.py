import sys, requests, base64, json
import config

from requests.auth import HTTPBasicAuth

def buildAuthUrl():
    cfg = config.readCfg()
    url = "https://accounts.spotify.com/authorize?response_type=code&client_id={}&redirect_uri={}".format(cfg['api']['client_id'], 'http://localhost')
    return url


# User Flow... Meh... (not needed, ups)
def getApiUserToken(code):
    cfg = config.readCfg()
    code = code.rsplit('?code=', 1)[1]
    base = "https://accounts.spotify.com/api/token"
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': 'http://localhost'
    }
    response = requests.post(base, data=data, auth=HTTPBasicAuth(cfg['api']['client_id'], cfg['api']['client_secret']))
    
    if response.status_code == 200:
        f = open("token.json", "w")
        f.write(response.text)
        f.close()
        print('INFO: token.json has been successfully written')
    else:
        exit("Meh... {} ({})".format(response.status_code, json.loads(response.text)["error"]))

def refreshApiToken():
    cfg = config.readCfg()
    refresh_token = config.getRefreshToken()
    base = "https://accounts.spotify.com/api/token"
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': cfg['api']['client_id']
    }
    response = requests.post(base, data=data, auth=HTTPBasicAuth(cfg['api']['client_id'], cfg['api']['client_secret']))
    
    if response.status_code == 200:
        f = open("token.json", "w")
        f.write(response.text)
        f.close()
        print('INFO: token.json has been successfully updated')
        return True
    else:
        exit("Meh... {} ({})".format(response.status_code, json.loads(response.text)["error"]))

# App Auth
def getApiToken():
    cfg = config.readCfg()
    base = "https://accounts.spotify.com/api/token"
    data = {
        'grant_type': 'client_credentials'
    }
    response = requests.post(base, data=data, auth=HTTPBasicAuth(cfg['api']['client_id'], cfg['api']['client_secret']))
    
    if response.status_code == 200:
        f = open("token.json", "w")
        f.write(response.text)
        f.close()
        print('INFO: token.json has been successfully written')
    else:
        exit("Meh... {} ({})".format(response.status_code, json.loads(response.text)["error"]))

if __name__ == '__main__':
    if len(sys.argv) == 1:
        getApiToken()
        exit()
        
    if len(sys.argv) == 2 and str(sys.argv[1]) == "--user":
         authUrl = buildAuthUrl()
         print("Please authorize your client at:\n{}".format(authUrl))
         exit()

    if len(sys.argv) == 2 and str(sys.argv[1]) == "--reauth":
        refreshApiToken()
        exit()

    if len(sys.argv) == 2:
        getApiUserToken(str(sys.argv[1]))
        exit()