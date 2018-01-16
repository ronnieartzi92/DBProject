import urllib2
import json
from urllib2 import Request, urlopen
from apiclient.discovery import build
from datetime import datetime
from dateutil import parser
import re

# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY2 = "AIzaSyCucB_A9LUg90yKMNZxVYePGdWghZFcODo"
DEVELOPER_KEY = "AIzaSyCOGtOfnRtzX4LcRa8VXFOOyFGujCRSlvc"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

YOUTUBE_LINK = 'https://www.youtube.com/watch?v={0}'


def find_lyrics(artist, name):
    try:
        print artist, name
        artist = str(artist).replace('/', '_')
        song_name_total = '{0}/{1}'.format(artist, name)
        # print song_name_total
        url = 'https://api.lyrics.ovh/v1/{0}'.format(song_name_total).replace(' ', '_')
        request = Request(url)
        response_body = urlopen(request).read()
        res = json.loads(response_body)
        lyrics = res['lyrics']
        return lyrics
    except Exception, e:
        print "error lyrics for {0}".format(song_name_total)
        print e
        return None


def youtube_search(artist, name):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
    query = '{0} {1}'.format(artist, name)
    try:
        search_response = youtube.search().list(q=query,part='id,snippet',maxResults=1,
                                                type='video', videoDuration='any').execute()
        #[u'nextPageToken', u'kind', u'items', u'regionCode', u'etag', u'pageInfo']
        search_result = search_response.get("items")[0]
        #[u'snippet', u'kind', u'etag', u'id']]
        #search_result['snippet'] = [u'thumbnails', u'title', u'channelId', u'publishedAt', u'liveBroadcastContent', u'channelTitle', u'description']
        video_id = search_result['id']['videoId']
        youtube_published_raw = parser.parse(search_result['snippet']['publishedAt'])
        image = search_result['snippet']['thumbnails']['medium']['url']
        youtube_published = datetime.strftime(youtube_published_raw, "%Y-%m-%d %X")
        youtube_description = search_result['snippet']['description']
        searchUrl="https://www.googleapis.com/youtube/v3/videos?id="+video_id+"&key="+DEVELOPER_KEY+"&part=contentDetails"
        response = urllib2.urlopen(searchUrl).read()
        data = json.loads(response)
        all_data = data['items']
        duration = all_data[0]['contentDetails']['duration']
        duration = re.findall('[0-9]*', duration)
        minutes = 0 if duration[2] == '' else int(duration[2])
        seconds = 0 if duration[4] == '' else int(duration[2])
        final_duration = int(minutes) * 60 + int(seconds)
        youtube_song = {'description': youtube_description, 'duration': final_duration,
                        'date_published': youtube_published, 'video_id': video_id, 'image': image}
        return youtube_song
    except Exception as e:
        print "error youtube for: {0}".format(query)
        print e

