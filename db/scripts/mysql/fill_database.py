from __future__ import print_function
import json
import mysql.connector
from db.entities.entities import *


class MysqlScripts:
    def __init__(self, user, database):
        self.user = user
        self.database = database

    def insert(self, path):

        # creating connection to db
        cnx = mysql.connector.connect(user=self.user, database=self.database)
        cursor = cnx.cursor()

        # inserting json file to db
        with open(path) as fp:
            json_file = json.load(fp)
            artists_list = json_file['artists']

            # Artist
            for artist_dict in artists_list:
                artist = Artist(artist_dict['name'], artist_dict['description'], artist_dict['img'], artist_dict['play_count'])
                artist_track_list = artist_dict['tracks']
                artist_event_list = artist_dict['events']
                artist_id = artist.insert(cursor)

                # Track
                for track_dict in artist_track_list:
                    track = Track(artist_id, track_dict['name'], track_dict['album'], track_dict['play_count'], track_dict['img'], track_dict['lyrics'], track_dict['description'])
                    tag_list = track_dict['tags']
                    youtube_dict = track_dict['youtube']
                    track_id = track.insert(cursor)

                    # Youtube
                    youtube = Youtube(track_id, youtube_dict['video_id'], youtube_dict['duration'], youtube_dict['date_published'], youtube_dict['description'])
                    youtube.insert(cursor)

                    # Tag
                    for tag_str in tag_list:
                        tag = Tag(tag_str)
                        tag_id = tag.find_id_by_name(cursor)
                        if tag_id is None: # Tag isn't in DB
                            tag_id = tag.insert(cursor)

                        # TrackToTag
                        track_to_tag = TrackToTag(track_id, tag_id)
                        track_to_tag.insert(cursor)

                # Event
                for event_dict in artist_event_list:
                    event = Event(artist_id, event_dict['location'], event_dict['date'], event_dict['url'], event_dict['description'], event_dict['title'])
                    event.insert(cursor)

        # closing resources
        cnx.commit()
        cursor.close()
        cnx.close()


if __name__ == "__main__":
    mysql_scripts = MysqlScripts('root', 'fogi')
    mysql_scripts.insert('collect_example.json')
