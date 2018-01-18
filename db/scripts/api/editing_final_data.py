import os
import json

'''
This scripts generates one .json file from many.
It is used for concatenating the collection files and verify that there are 
no artists multiples
'''


class GenerateJson:
    def __init__(self):
        self.all_artists = []
        self.final = {'artists': []}
 
    def edit(self):
        # open each file in the library and loads it
        for file in os.listdir('.'):
            if file == 'editing_final_data.py':
                continue
            with open(file, 'r') as feedsjson:
                artists = json.load(feedsjson)

            # Verify that are nu duplicates
            for item in artists['artists']:
                if item['name'] not in self.all_artists:
                    self.all_artists.append(item['name'])
                    self.final['artists'].append(item)

        for item in self.final['artists']:
            if item['events'] is None:
                item['events'] = []

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
