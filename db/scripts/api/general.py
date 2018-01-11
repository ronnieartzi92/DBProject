import urllib
import requests
import os
import apiclient

#features
"https://www.last.fm/api"

last_fm_creds = {"Application_name":	"songs track",
                "API_key": "ef0a6c7bc22d825341b9aef3cbb7c349",
                "Shared_secret": "2ee483bd607f0693f0cc8aa7d74a1cd9",
                "Registered_to": "fogelomer"}

#youtube
YOUTUBE1 = "https://developers.google.com/youtube/v3/docs/search/list"
"https://developers.google.com/youtube/v3/docs/search#resource"

youtube_creds = {"apii_key": "AIzaSyCucB_A9LUg90yKMNZxVYePGdWghZFcODo",
                 "Oauth_id": "689564199519-41keah26kj7jl05k3jr5g0u6go0pv7hu.apps.googleusercontent.com",
                 "Oauth_secret": "Z0bohbkOB-0o3l0Gs4_IUMX4"}
#lyrics
"http://api.musixmatch.com/ws/1.1/" #api cost money

#events - wait for key.
SONGKICK_ART = "http://api.songkick.com/api/3.0/artists/{0}/calendar.json?apikey={1}" #0 artist 1 api_key
SONGKICK_brainz = "http://api.songkick.com/api/3.0/artists/mbid:{music_brainz_id}/calendar.json?apikey={your_api_key}"



