import config, spotify
import json, datetime

from podgen import Podcast, Episode, Media

def getShows():
    cfg = config.readCfg()
    for showId in cfg['shows']:
        show = spotify.getShow(showId)

        if config.debug():
            print(show["name"])
            print(show["description"])
        

        eps = show["episodes"]["items"]

        p = Podcast(
            name=show["name"],
            description=show["description"],
            website=show["external_urls"]["spotify"],
            explicit=show["explicit"],
            image=show["images"][0]["url"],
            language=show["languages"][0],
            withhold_from_itunes=True,
        )

        for ep in eps:
            print(ep["name"])
            p.episodes += [
                Episode(
                    title=ep["name"],
                    media=Media(spotify.getMediaUrl(ep["audio_preview_url"]), type="audio/mpeg"),
                    summary=ep["description"],
                    explicit=ep["explicit"],
                    # publication_date=datetime.date(ep["release_date"]), Meh... tidi               
                )
            ]


        write("{}/{}.xml".format(cfg['export'], showId), p.rss_str())
        #print(json.dumps(eps, indent=4))


        
        
def write(filename, content):
    f = open(filename, "w")
    f.write(content)
    f.close()

if __name__ == '__main__':
    getShows()