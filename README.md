# unexclusivy-spotify-podcasts
Generates an RSS feed that can be subscribed in your favorite podcast app

How to run:
-----------
### Install
```
~/unexclusivy-spotify-podcasts$ python3 -m venv env
~/unexclusivy-spotify-podcasts$ source env/bin/activate
~/unexclusivy-spotify-podcasts$ pip install -r requirements.txt
~/unexclusivy-spotify-podcasts$ cp config.sample.json config.json
```
and customize config.json accordingly

### API Authentication
- Get your API keys at https://developer.spotify.com/dashboard/applications
- Add your API client ID and secret to config.json
- Run auth.py
```
(env) ~/unexclusivy-spotify-podcasts$ python auth.py 
INFO: token.json has been successfully written
```

### Run
```
~/unexclusivy-spotify-podcasts$ unexclusivy-spotify-podcasts/env/bin/python python run.py
```

Known Issues:
-------------
- Media URLs don't have file extensions ->  Apple Podcasts will fail to download the episodes (streaming still works) -> [Fix](../master/docs/ApplePodcasts_Fix/README.md)

###### _Spotify® is a trademark of Spotify AB which does not sponsor, authorize, or endorse this project._
