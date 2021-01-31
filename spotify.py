import config, auth
import requests, json, os

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

def getMediaSize(audio_preview_url):
    fileId = audio_preview_url.rsplit('/', 1)[1]
    mediaUrl = "https://anon-podcast.scdn.co/{}".format(fileId)
    # Check Cache
    try:
        f=open(os.path.dirname(os.path.realpath(__file__))+'/cache.txt', 'r')
    except FileNotFoundError:
        f=open(os.path.dirname(os.path.realpath(__file__))+'/cache.txt', 'w+')

    # check cache
    lines = f.readlines()
    for x in lines:
        if x.startswith(fileId):
            length = x.split("|")[1]
            found = True
            # found in cache
            return length
    # not found in cache
    f.close
    response = requests.head(mediaUrl)
    length = response.headers["Content-Length"]
    f=open(os.path.dirname(os.path.realpath(__file__))+'/cache.txt', 'a')
    f.write("{}|{}\n".format(fileId, length)) # write to cache
    f.close
    return length