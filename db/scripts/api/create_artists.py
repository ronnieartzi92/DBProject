import json
from urllib2 import Request, urlopen
from songs_extra import find_lyrics, youtube_search
from events import get_events

LAST_FM_API = 'ef0a6c7bc22d825341b9aef3cbb7c349'

'''
This script generates the data from different APIs.
the data is from structure:
    { 'artists':
                ['events': [ {'country': , 'city': , 'venue': , 'url': , 'img' , 'title': } ],
                 'tracks': [ {'name': , 'album': , 'play_count': , 'img': , 'lyrics': , 'description': ,
                              youtube: { 'duration': , 'video_id': , 'date_published': } , 'tags': } ].
                 'name':
                 'play_count':
    }           ]

the data is collected in a nested way - starting from artists and it's details (data.get_atrists()) - from last.fm,
then collecting X events for each artist and their details (get_events()) - from eventful.com,
collecting X tracks for each artists, for each track collecting:
track details (get_tracks()) - from last.fm,
track lyrics (find_lyrics()) - from lyrics.ovh,
track youtube details (youtube_search()) - from youtube.com

output is written for every 10 artists.
'''


class Data:
    def __init__(self):
        self.all_tags = []
        self.all_songs = []
        self.artists = []
        self.all_artists = []
        self.art_count = 1

    def get_artsits(self):
        '''
        generating the artists objects list.
        :return: None, json file is the output
        '''
        try:
            with open('final.json', 'r') as feedsjson:
                artists = json.load(feedsjson)
            for item in artists['artists']:
                self.all_artists.append(item['name'])
            with open('final2.json', 'r') as feedsjson:
                artists = json.load(feedsjson)
            for item in artists['artists']:
                self.all_artists.append(item['name'])
            with open('final3.json', 'r') as feedsjson:
                artists = json.load(feedsjson)
            for item in artists['artists']:
                self.all_artists.append(item['name'])
            for i in ['1']:
                try:
                    # getting artists list from last.fm
                    request = Request("http://ws.audioscrobbler.com/2.0/?method=chart.gettopartists&limit={0}&api_key={1}&page={2}&format=json".format(
                                      '940', LAST_FM_API, i))
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
                            self.all_artists.append(name)
                            # reformatting artist name for future queries
                            art = name.replace(' ', '%20').encode('utf-8')
                            req = Request("http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist={0}&api_key={1}&format=json".format(
                                        art, LAST_FM_API))
                            response_body = json.loads(urlopen(req).read())['artist']

                            # getting artist info
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

                            # getting artist events
                            events = []
                            try:
                                events = get_events(artist['name'])
                            except Exception as e:
                                print "cannot get events for artists: {0}".format(artist['name'])
                                print e

                            # getting artist tracks
                            try:
                                tracks = self.get_tracks(art)
                                if tracks is None:
                                    continue
                            except Exception as e:
                                print "cannot get tracks for artists: {0}".format(artist['name'])
                                print e
                                continue  # continue to next artists if there's no tracks

                            # generating the track object and insert it the the collected data
                            new_artist = {'name': name, 'description': desc, 'img': image,
                                          'play_count': play_count, 'tracks': tracks,
                                          'events': events}
                            self.artists.append(new_artist)
                        except Exception as e:
                            print "cannot generate artist {0}".format(artist['name'])
                            print e
                            continue  # continue to next artists if exception raised

                        # print data to file every 10 artists
                        self.art_count += 1
                        if self.art_count % 10 == 0:
                            result = {"artists": self.artists}
                            filename = "artists{0}-{1}.json".format(i, self.art_count)
                            with open(filename, 'w') as feedsjson:
                                json.dump(result, feedsjson)
                            print "for file {0}".format(filename)
                            self.print_stats()

                # printing last file if exception raised before next 10 artists
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
        # continue to next artists page query
        except Exception as e:
            print "cannot get top artists"
            print self.print_stats()
            print e

    def get_tracks(self, artist):
        '''
        this function generating tracks list for every artist
        :param artist: the artist name (string)
        :return: track objects list
        '''
        try:
            art = artist.replace(' ', '%20')
            result = []
            request = Request("http://ws.audioscrobbler.com/2.0/?method=artist.gettoptracks&artist={0}&limit={1}&api_key={2}&format=json".format(
                              art, '70', LAST_FM_API))
            response_body = json.loads(urlopen(request).read())
            raw_tracks = response_body['toptracks']
            tracks = raw_tracks['track']
            for track in tracks:
                try:
                    # reformatting the track name for future queries
                    name = track['name'].encode('utf-8')
                    track_search_name = name.replace(' ', '%20')
                    req = Request("http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key={0}&artist={1}&track={2}&format=json".format(
                                LAST_FM_API, art, track_search_name))
                    response_body = json.loads(urlopen(req).read())['track']
                    info = response_body
                    # getting track tags
                    tags = [tag['name'] for tag in info['toptags']['tag']]
                    self.all_tags += tags

                    # getting track info
                    desc = None
                    if 'wiki' in info:
                        desc = info['wiki']['content']
                    album = None
                    if 'album' in info:
                        album = info['album']['title']

                    # getting track youtube details
                    try:
                        youtube = youtube_search(artist.replace('%20', ' '), name)
                        if youtube is None:
                            continue
                    except Exception as e:
                        print "cannot get youtube for track: {0}".format(artist+'/'+name)
                        print e
                        continue
                    image = youtube['image']
                    del youtube['image']

                    # getting track lyrics
                    lyrics = None
                    try:
                        lyrics = find_lyrics(artist, name)
                    except Exception as e:
                        print "cannot get lyrics for track: {0}".format(artist + '/' + name)
                        print e
                    # generating the track object and insert it the the collected data
                    new_track = {'name': info['name'], 'album': album, 'img': image, 'tags': tags,
                                 'play_count': info['playcount'], 'description': desc,
                                 'lyrics': lyrics, 'youtube': youtube}
                    result.append(new_track)
                    self.all_songs.append(new_track)
                except Exception as e:
                    print "error getting track: {0}".format(name)
                    print e
                    continue  # continue to next song if failed
            return result
        except Exception, e:
            print "error getting tracks for: {0}".format(artist)
            print e
            return None

    def print_stats(self):
        '''
        printing stats and resetting the data
        :return:
        '''
        print "total tags: {0}".format(len(set(self.all_tags)))
        print "total artists: {0}".format(len(self.artists))
        print "total songs: {0}".format(len(self.all_songs))
        self.all_tags = []
        self.all_songs = []
        self.artists = []


# script main
my_data = Data()
my_data.get_artsits()

