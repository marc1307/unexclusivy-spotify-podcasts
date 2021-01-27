import config
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
    url = baseUrl+"/shows/{}".format(showId)
    if config.debug():
        print("DEBUG: getShow() - URL {}".format(url))
    headers = buildHeaders()
    response = requests.request("GET", url, headers=headers)
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        exit("Meh... {} ({})".format(response.status_code, json.loads(response.text)["error"]["message"]))

def getShowEpisodes(showId):
    cfg = config.readCfg()
    url = baseUrl+"/shows/{}/episodes".format(showId)
    if config.debug():
        print("DEBUG: getShowEpisodes() - URL {}".format(url))
    headers = buildHeaders()
    response = requests.request("GET", url, headers=headers)
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        exit("Meh... {} ({})".format(response.status_code, json.loads(response.text)["error"]["message"]))


def getMediaUrl(audio_preview_url):
    base = "https://anon-podcast.scdn.co/"
    fileId = audio_preview_url.rsplit('/', 1)[1] 
    out = base + fileId
    return out
    