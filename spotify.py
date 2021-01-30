import config, auth
import requests, json

baseUrl = 'https://api.spotify.com/v1'

def buildHeaders():
    token = config.readToken()
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': "Bearer {}".format(token)
    }
    return headers

def getShow(showId):
    cfg = config.readCfg()
    url = baseUrl+"/shows/{}?market={}".format(showId, cfg["market"])
    headers = buildHeaders()
    response = requests.request("GET", url, headers=headers)
    if response.status_code == 200:
        return json.loads(response.text)
    elif response.status_code == 401:
        error = json.loads(response.text)["error"]["message"]
        if error == "The access token expired":
            print("INFO: Token refresh required")
            auth.getApiToken()
            headers = buildHeaders()
            response = requests.request("GET", url, headers=headers)
            if response.status_code == 200:
                return json.loads(response.text)
    else:
        exit("Meh... {} ({})".format(response.status_code, json.loads(response.text)["error"]["message"]))

def getShowEpisodes(showId):
    cfg = config.readCfg()
    url = baseUrl+"/shows/{}/episodes".format(showId)
    headers = buildHeaders()
    response = requests.request("GET", url, headers=headers)
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        exit("Meh... {} ({})".format(response.status_code, json.loads(response.text)["error"]["message"]))

def getMediaUrl(audio_preview_url):
    cfg = config.readCfg()
    base = cfg["spotify"]["mediaBaseURL"]
    ext = cfg["spotify"]["mediaFileExtension"]
    fileId = audio_preview_url.rsplit('/', 1)[1]
    out = base + fileId + ext
    return out