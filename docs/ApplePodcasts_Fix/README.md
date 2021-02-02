# Apple Podcast Fix
If the URL of the media file does not have a file extension Apple Podcasts will not download the media.

You can change the media base URL in config.json, this allows you to use a proxy.
The proxy needs to strip the file extension and change the hostname to the original CDN hostname before forwarding it to Spotify.

```
error	10:50:58.255959+0100	Podcasts	Validation failed with error Invalid asset: The original extension and resolved extension were not playable for episode url Optional(https://anon-podcast.scdn.co/099169162529dd064475edb69b80f979fa6c8d76)
default	10:50:58.255987+0100	Podcasts	Post download file validation failed, error: Invalid asset: The original extension and resolved extension were not playable for episode url Optional(https://anon-podcast.scdn.co/099169162529dd064475edb69b80f979fa6c8d76)
error	10:50:58.257960+0100	Podcasts	Download failed due to error: Invalid asset: The original extension and resolved extension were not playable for episode url Optional(https://anon-podcast.scdn.co/099169162529dd064475edb69b80f979fa6c8d76).
```
https://help.apple.com/itc/podcasts_connect/#/itcb54353390
https://itunespartner.apple.com/podcasts/articles/podcast-requirements-3058


## config.json Example:
```
...
    "spotify": {
        "mediaBaseURL": "https://my-awesome-proxy.com/",
        "mediaFileExtension": ".mp3"
    }
...
```

## Proxy Config Examples:
### Apache
TBD

### Nginx
TBD

### Citrix ADC Netscaler
```
# rewrites / replace hostname and strip file extension
add rewrite action rw_act_dl-proxy_changeHostname replace http.REQ.HOSTNAME "\"anon-podcast.scdn.co\""
add rewrite action rw_act_dl-proxy_removeFileExtension replace http.REQ.URL.PATH "http.REQ.URL.PATH.BEFORE_STR(\".mp3\")"
add rewrite policy rw_pol_dl-proxy_changeHost "http.REQ.HOSTNAME.EQ(\"my-awesome-proxy.com\")" rw_act_dl-proxy_changeHostname
add rewrite policy rw_pol_dl-proxy_removeFileExt "http.REQ.URL.PATH.ENDSWITH(\".mp3\")" rw_act_dl-proxy_removeFileExtension

# reponder / filter requests that do not point directly to media (prevent bots, etc)
add responder action resp_403 respondwithhtmlpage res_html_403 -responseStatusCode 403
add responder policy resp_pol_dl-proxy_dropInvalidRequests "http.REQ.URL.EQ(\"/\") || http.REQ.URL.SET_TEXT_MODE(ignorecase).ENDSWITH(\".mp3\").NOT || http.REQ.URL.SET_TEXT_MODE(ignorecase).BEFORE_STR(\".mp3\").REGEX_MATCH(re/[0-9a-f]{40}/).NOT" resp_403

# add server
add server EXT_tm_srv-anon-podcast.scdn.co anon-podcast.scdn.co

# add service
add service EXT_tm_lb_src-anon-podcast.scdn.co EXT_tm_srv-anon-podcast.scdn.co SSL 443 -gslb NONE -maxClient 0 -maxReq 0 -cip DISABLED -usip NO -useproxyport YES -sp OFF -cltTimeout 180 -svrTimeout 360 -CKA NO -TCPB NO -CMP NO

# add vserver
add lb vserver EXT_tm_lb_srv-anon-podcast.scdn.co HTTP 0.0.0.0 0 -persistenceType NONE -cltTimeout 180
bind lb vserver EXT_tm_lb_srv-anon-podcast.scdn.co EXT_tm_lb_src-anon-podcast.scdn.co

bind lb vserver EXT_tm_lb_srv-anon-podcast.scdn.co -policyName resp_pol_dl-proxy_dropInvalidRequests -priority 100 -gotoPriorityExpression END -type REQUEST
bind lb vserver EXT_tm_lb_srv-anon-podcast.scdn.co -policyName rw_pol_dl-proxy_changeHost -priority 100 -gotoPriorityExpression NEXT -type REQUEST
bind lb vserver EXT_tm_lb_srv-anon-podcast.scdn.co -policyName rw_pol_dl-proxy_removeFileExt -priority 110 -gotoPriorityExpression END -type REQUEST
```