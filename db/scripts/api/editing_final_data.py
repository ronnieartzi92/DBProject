import os
import json

'''
This scripts generates one .json file from many.
It is used for concatenating the collection files and verify that there are 
no artists multiples
'''


elctrify_dundun = { 'name': 'elctrify_dundun',
                    'play_count': 1950000,
                    'events': [],
                    'tracks': [{'name': 'The Clash Royale Song',
                                'album': 'elctrify',
                                'lyrics': '',
                                'description': 'The Best Clash Royale Player with the best sing',
                                'play_count': 195000,
                                'img': 'https://i.ytimg.com/vi/tv4UDi1TNy4/hqdefault.jpg',
                                'youtube': {
                                            'duration': 205,
                                            'video_id': 'd_AWJJWDqFo',
                                            'date_published': '2018-01-19 00:00:01'
                                            }
                                }]
                    }



class GenerateJson:
    def __init__(self):
        self.all_artists = []
        self.final = {'artists': []}
 
    def edit(self):
        # open each file in the library and loads it
        for file in os.listdir('.'):
            if file in ['editing_final_data.py', 'songs_extra.py', 'events.py', 'create_artists.py']:
                continue
            print file
            with open(file, 'r') as feedsjson:
                artists = json.load(feedsjson)

            # Verify that are nu duplicates
            for item in artists['artists']:
                local_songs = []
                if item['name'] not in self.all_artists:
                    if item['tracks'] == []:
                        continue
                    for song in item['tracks']:
                        if song['name'] in local_songs:
                            item['tracks'].remove(song)
                        else:
                            local_songs.append(song['name'])

                    self.all_artists.append(item['name'])
                    self.final['artists'].append(item)

        for item in self.final['artists']:
            if item['events'] is None:
                item['events'] = []

        self.final['artists'].append(elctrify_dundun)

        # printing stats
        print len(self.all_artists)
        print len(self.final['artists'])
        count = 0
        for item in self.final['artists']:
            count += len(item['tracks'])
        print count

        # writing final file for inserting to Db.
        with open('final_full.json', 'w') as feedsjson:
            json.dump(self.final, feedsjson)



# script main
generator = GenerateJson()
generator.edit()
