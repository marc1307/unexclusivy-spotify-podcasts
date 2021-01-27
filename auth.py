import sys, requests, base64, json
import config

from requests.auth import HTTPBasicAuth

def buildAuthUrl():
    cfg = config.readCfg()
    url = "https://accounts.spotify.com/authorize?response_type=code&client_id={}&redirect_uri={}".format(cfg['api']['client_id'], 'http://localhost')
    return url

def getApiToken(code):
    cfg = config.readCfg()
    code = code.rsplit('=', 1)[1]
    base = "https://accounts.spotify.com/api/token"
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': 'http://localhost'
    }
    reponse = requests.post(base, data=data, auth=HTTPBasicAuth(cfg['api']['client_id'], cfg['api']['client_secret']))
    
    if reponse.status_code == 200:
        f = open("token.json", "w")
        f.write(reponse.text)
        f.close()
    else:
        exit("Meh... {} ({})".format(reponse.status_code, json.loads(reponse.text)["error"]))


if __name__ == '__main__':
    if len(sys.argv) == 1:
        authUrl = buildAuthUrl()
        print("URL: {}".format(authUrl))

    if len(sys.argv) == 2:
        getApiToken(str(sys.argv[1]))