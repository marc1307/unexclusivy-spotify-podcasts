# unexclusivy-spotify-podcasts
Generates a RSS Feed that can be subscribed in any podcast app

How to run:
-----------
## Install
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
- Spotify API does not provide file size for Media
- Media URLs don't have file extension ->  Apple Podcasts will fail to download the episodes (streaming still works)
```
error	10:50:58.255959+0100	Podcasts	Validation failed with error Invalid asset: The original extension and resolved extension were not playable for episode url Optional(https://anon-podcast.scdn.co/099169162529dd064475edb69b80f979fa6c8d76)
default	10:50:58.255987+0100	Podcasts	Post download file validation failed, error: Invalid asset: The original extension and resolved extension were not playable for episode url Optional(https://anon-podcast.scdn.co/099169162529dd064475edb69b80f979fa6c8d76)
error	10:50:58.257960+0100	Podcasts	Download failed due to error: Invalid asset: The original extension and resolved extension were not playable for episode url Optional(https://anon-podcast.scdn.co/099169162529dd064475edb69b80f979fa6c8d76).
```

###### _Spotify® is a trademark of Spotify AB which does not sponsor, authorize, or endorse this project._
