import urllib2
import json
from urllib2 import Request, urlopen
# in order to use please install google-api-python-client(1.6.4) from pip
from apiclient.discovery import build
from datetime import datetime
from dateutil import parser
import re


DEVELOPER_KEY = "AIzaSyCucB_A9LUg90yKMNZxVYePGdWghZFcODo"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
YOUTUBE_LINK = 'https://www.youtube.com/watch?v={0}'


def find_lyrics(artist, name):
    '''
    A simple api request for artists/song_name which return lyrics if exists
    :param artist: artist name (string)
    :param name: song name (string)
    :return: lyrics string
    '''
    try:
        print artist, name
        artist = artist.replace('/', '_')
        song_name_total = '{0}/{1}'.format(artist, name)
        url = 'https://api.lyrics.ovh/v1/{0}'.format(song_name_total).replace(' ', '_')
        request = Request(url)
        response_body = urlopen(request).read()
        res = json.loads(response_body)
        lyrics = res['lyrics']
        return lyrics
    except Exception, e:
        print "error lyrics for {0}".format(song_name_total)
        print e


def youtube_search(artist, name):
    '''
    function which takes artist and song name and return the most relevant youtube object.
    :param artist: artist name (string)
    :param name: song name (string)
    :return: youtube object
    '''

    # creating youtube api agent and query.
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
    query = '{0} {1}'.format(artist, name)
    try:
        # searching for the first (most relevant) answer for each song.
        search_response = youtube.search().list(q=query, part='id,snippet', maxResults=1,
                                                type='video', videoDuration='any').execute()
        search_result = search_response.get("items")[0]

        # getting youtube detilas
        video_id = search_result['id']['videoId']
        youtube_published_raw = parser.parse(search_result['snippet']['publishedAt'])
        youtube_published = datetime.strftime(youtube_published_raw, "%Y-%m-%d %X")
        image = search_result['snippet']['thumbnails']['medium']['url']
        youtube_description = search_result['snippet']['description']

        # making another request for youtube duration from video_id deatils
        search_url = "https://www.googleapis.com/youtube/v3/videos?id={0}&key={1}&part=contentDetails".format(
                                                                                video_id, DEVELOPER_KEY)
        response = urllib2.urlopen(search_url).read()
        data = json.loads(response)
        all_data = data['items']
        duration = all_data[0]['contentDetails']['duration']

        # reformatting the duration for seconds.
        duration = re.findall('[0-9]*', duration)
        minutes = 0 if duration[2] == '' else int(duration[2])
        seconds = 0 if duration[4] == '' else int(duration[4])
        final_duration = int(minutes) * 60 + int(seconds)
        # generating youtube object and return it.
        youtube_song = {'description': youtube_description, 'duration': final_duration,
                        'date_published': youtube_published, 'video_id': video_id, 'image': image}
        return youtube_song
    # returning None in case of error which will erase the track from the DB.
    except Exception as e:
        print "error youtube for: {0}".format(query)
        print e
        return None
