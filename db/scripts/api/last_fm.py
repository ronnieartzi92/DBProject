import json
from urllib2 import Request, urlopen
from songs_extra import find_lyrics, youtube_search
from events import get_events
import datetime

LAST_FM_API = 'ef0a6c7bc22d825341b9aef3cbb7c349'

class data():
    def __init__(self):
        self.all_tags = []
        self.all_songs = []
        self.artists = []
        self.all_artists = []
        self.art_count = 1

    def get_artsits(self):
        try:
            with open('final.json', 'r') as feedsjson:
                artists = json.load(feedsjson)

            for item in artists['artists']:
                self.all_artists.append(item['name'])
            for i in range(1, 5):
                try:
                    request = Request("http://ws.audioscrobbler.com/2.0/?method=chart.gettopartists&limit={0}&api_key={1}&page={2}&format=json".format(
                                      '1000', LAST_FM_API, i))
                    response_body = urlopen(request).read()
                    res = json.loads(response_body)
                    raw_arstits = res['artists']
                    artists = raw_arstits['artist']
                    result = None
                    for artist in artists:
                        try:
                            name = artist['name']
                            if name in self.all_artists:
                                continue
                            if name in ['W&W']:
                                continue
                            self.all_artists.append(name)
                            art = name.replace(' ', '%20').encode('utf-8')
                            req = Request("http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist={0}&api_key={1}&format=json".format(
                                        art, LAST_FM_API))
                            response_body = json.loads(urlopen(req).read())['artist']
                            desc = ''
                            play_count = 0
                            image = None
                            info = response_body
                            try:
                                desc = info['bio']['content']
                            except:
                                print 'no description for {0}'.format(name)
                            try:
                                play_count = info['stats']['playcount']
                            except:
                                print 'no play_count for {0}'.format(name)
                            try:
                                image = info['image'][1]['#text']
                            except:
                                print 'no image for {0}'.format(name)
                            events = []
                            try:
                                events = get_events(artist['name'])
                            except Exception as e:
                                print "cannot get events for artists: {0}".format(artist['name'])
                                print e
                            try:
                                tracks = self.get_tracks(artist['name'])
                                if tracks is None:
                                    continue
                            except Exception as e:
                                print "cannot get tracks for artists: {0}".format(artist['name'])
                                print e
                                continue
                            new_artist = {'name': name, 'description': desc, 'img': image,
                                          'play_count': play_count, 'tracks': tracks,
                                          'events': events}
                            self.artists.append(new_artist)
                        except Exception as e:
                            print "cannot generate artist {0}".format(artist['name'])
                            print e
                            continue
                        self.art_count += 1
                        if self.art_count % 10 == 0:
                            result = {"artists": self.artists}
                            filename = "artists{0}-{1}.json".format(i, self.art_count)
                            with open(filename, 'w') as feedsjson:
                                json.dump(result, feedsjson)
                            print "for file {0}".format(filename)
                            self.print_stats()
                except Exception as e:
                    filename = "artists{0}-{1}-end.json".format(i, self.art_count)
                    if result is None:
                        result = {"artists": self.artists}
                    with open(filename, 'w') as feedsjson:
                        json.dump(result, feedsjson)
                    print "page {0} didn't finished totally".format(i)
                    print self.print_stats()
                    print e
                    continue
        except Exception as e:
            print "cannot get top artists"
            print self.print_stats()
            print e

    def get_tracks(self, artist):
        try:
            art = artist.replace(' ', '%20')
            result = []
            request = Request("http://ws.audioscrobbler.com/2.0/?method=artist.gettoptracks&artist={0}&limit={1}&api_key={2}&format=json".format(
                              art, '35', LAST_FM_API))
            response_body = json.loads(urlopen(request).read())
            raw_tracks = response_body['toptracks']
            tracks = raw_tracks['track']
            for track in tracks:
                try:
                    name = track['name'].encode('utf-8')
                    track_search_name = name.replace(' ', '%20')
                    req = Request("http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key={0}&artist={1}&track={2}&format=json".format(
                                LAST_FM_API, art, track_search_name))
                    response_body = json.loads(urlopen(req).read())['track']
                    info = response_body
                    tags = [tag['name'] for tag in info['toptags']['tag']]
                    self.all_tags += tags
                    desc = None
                    if 'wiki' in info:
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
                    image = youtube['image']
                    del youtube['image']
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
                    continue
            return result
        except Exception, e:
            print "error getting tracks for: {0}".format(artist)
            print e
            return None

    def print_stats(self):
        print "total tags: {0}".format(len(set(self.all_tags)))
        print "total artists: {0}".format(len(self.artists))
        print "total songs: {0}".format(len(self.all_songs))
        self.all_tags = []
        self.all_songs = []
        self.artists = []
        self.art_count = 1

my_data = data()
my_data.get_artsits()

