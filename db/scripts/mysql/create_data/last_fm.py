import json
import general
from urllib2 import Request, urlopen
from songs_extra import find_lyrics, youtube_search
from events import get_events
import datetime

LAST_FM_API = 'ef0a6c7bc22d825341b9aef3cbb7c349'

class data():
    def __init__(self):
        self.all_tags = []
        self.all_songs = []
        self.songs_to_tags = {}
        self.artists = []

    def get_artsits(self):
        try:
            request = Request("http://ws.audioscrobbler.com/2.0/?method=chart.gettopartists&limit={0}&api_key={1}&format=json".format(
                              '50', LAST_FM_API))
            response_body = urlopen(request).read()
            res = json.loads(response_body)
            raw_arstits = res['artists']
            artists = raw_arstits['artist']
            for artist in artists:
                name = artist['name']
                req = Request("http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist={0}&api_key={1}&format=json".format(
                                name, LAST_FM_API))
                response_body = json.loads(urlopen(req).read())['artist']
                info = response_body
                events = None
                tracks = None
                try:
                    events = get_events(artist['name'])
                except Exception as e:
                    print "cannot get events for artists; {0}".format(artist['name'])
                    print e
                try:
                    tracks = self.get_tracks(artist['name'])
                    if tracks is None:
                        continue
                except Exception as e:
                    print "cannot get tracks for artists; {0}".format(artist['name'])
                    print e
                    continue
                new_artist = {'name': name, 'description': info['bio']['content'], 'img': info['image'][1]['#text'],
                              'play_count': info['stats']['playcount'], 'tracks': tracks,
                              'events': events}
                if artist not in self.artists:
                    self.artists.append(new_artist)
            res = {"artists": self.artists}
            with open("artists.json", 'w') as feedsjson:
                json.dump(res, feedsjson)
        except Exception as e:
            print "cannot get top artists"
            print e

    def get_tracks(self, artist):
        try:
            art = artist.replace(' ', '%20')
            result = []
            request = Request("http://ws.audioscrobbler.com/2.0/?method=artist.gettoptracks&artist={0}&limit={1}&api_key={2}&format=json".format(
                              art, '50 ', LAST_FM_API))
            response_body = json.loads(urlopen(request).read())
            raw_tracks = response_body['toptracks']
            tracks = raw_tracks['track']
            for track in tracks:
                try:
                    name = track['name']
                    image = track['image'][2]['#text']
                    track_search_name = name.replace(' ', '%20')
                    req = Request("http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key={0}&artist={1}&track={2}&format=json".format(
                                     general.last_fm_creds.get('API_key'), art, track_search_name))
                    response_body = json.loads(urlopen(req).read())['track']
                    info = response_body
                    tags = [tag['name'] for tag in info['toptags']['tag']]
                    self.all_tags += tags
                    date = None
                    desc = None
                    if 'wiki' in info:
                        date = info['wiki']['published']
                        desc = info['wiki']['content']
                    album = None
                    if 'album' in info:
                        album = info['album']['title']
                    try:
                        youtube = youtube_search(artist, name)
                        if youtube is None:
                            continue
                    except Exception as e:
                        print "cannot get youtube for track: {0}".format(artist+'/'+name)
                        print e
                        continue
                    lyrics = None
                    try:
                        lyrics = find_lyrics(artist, name)
                    except Exception as e:
                        print "cannot get lyrics for track: {0}".format(artist + '/' + name)
                        print e
                    new_track = {'name': info['name'], 'album': album, 'img': image, 'tags': tags,
                                 'play_count': info['playcount'], 'description': desc, 'lyrics': lyrics, 'youtube': youtube}
                    result.append(new_track)
                    self.all_songs.append(new_track)
                except Exception as e:
                    print "error getting track: {0}".format(name)
                    print e
            return result
        except Exception, e:
            print "error getting tracks for: {0}".format(artist)
            print e

    def print_stats(self):
        print "total tags: {0}".format(len(set(self.all_tags)))
        print "total artists: {0}".format(len(self.artists))
        print "total songs: {0}".format(len(self.all_songs))

my_data = data()
my_data.get_artsits()
my_data.print_stats()

