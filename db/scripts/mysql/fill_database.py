from __future__ import print_function
import json
import os

import mysql.connector
from db.entities.entities import *


class MysqlScripts:
    def __init__(self, user, database):
        self.user = user
        self.database = database
        self.artists = 0
        self.tracks = 0
        self.tags = 0
        self.yotubes = 0
        self.tracks_to_tags = 0
        self.events = 0
        self.tracks_isam = 0



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
                artist = Artist(artist_dict['name'], artist_dict['play_count'])
                artist_track_list = artist_dict['tracks']
                artist_event_list = artist_dict['events']
                try:
                    artist_id = artist.insert(cursor)
                    self.artists += 1
                    if self.artists % 50 == 0:
                        print("Entered " + str(self.artists) + " Artists")
                except Exception as e:
                    MysqlScripts.print_entity(e, artist)
                    continue


                # Track
                for track_dict in artist_track_list:
                    track = Track(artist_id, track_dict['name'], track_dict['album'], track_dict['play_count'], track_dict['img'], track_dict['lyrics'], track_dict['description'])
                    tag_list = track_dict['tags']
                    youtube_dict = track_dict['youtube']
                    try:
                        track_id = track.insert(cursor)
                        self.tracks += 1
                    except Exception as e:
                        MysqlScripts.print_entity(e, track)
                        continue

                    # Track_ISAM - for full text search
                    track_isam = TrackIsam(track)
                    try:
                        track_isam.insert(cursor)
                        self.tracks_isam += 1
                    except Exception as e:
                        MysqlScripts.print_entity(e, track_isam)
                        continue

                    # Youtube
                    youtube = Youtube(track_id, youtube_dict['video_id'], youtube_dict['duration'], youtube_dict['date_published'])
                    try:
                        youtube.insert(cursor)
                        self.yotubes += 1
                    except Exception as e:
                        MysqlScripts.print_entity(e, youtube)
                        continue

                    # Tag
                    for tag_str in tag_list:
                        tag = Tag(tag_str)
                        tag_id = tag.find_id_by_name(cursor)
                        if tag_id is None: # Tag isn't in DB
                            try:
                                tag_id = tag.insert(cursor)
                                self.tags += 1
                            except Exception as e:
                                MysqlScripts.print_entity(e, tag)
                                continue

                        # TrackToTag
                        track_to_tag = TrackToTag(track_id, tag_id)
                        try:
                            track_to_tag.insert(cursor)
                            self.tracks_to_tags += 1
                        except Exception as e:
                            MysqlScripts.print_entity(e, track_to_tag)
                            continue

                # Event
                for event_dict in artist_event_list:
                    event = Event(artist_id, event_dict['country'], event_dict['city'], event_dict['venue'], event_dict['date'], event_dict['url'], event_dict['title'], event_dict['img'])
                    try:
                        event.insert(cursor)
                        self.events += 1
                    except Exception as e:
                        MysqlScripts.print_entity(e, event)
                        continue

        # closing resources
        cnx.commit()
        cursor.close()
        cnx.close()

    def insert_folder(self, folder):
        for file in os.listdir(folder):
            full_path = folder + '/' + file
            print(">>>>>>>>>>>>>>>>>>> Starting", full_path)
            self.insert(full_path)
            print("<<<<<<<<<<<<<<<<<<< Done", full_path)

    @staticmethod
    def print_entity(exp, obj):
        print("------------------------------------------- Exception-----------------------------------------")
        print(exp)
        print("class:", obj.__class__)
        for key in obj.__dict__:
            print(key + ":", obj.__dict__[key])
        print("----------------------------------------------------------------------------------------------")

    def __repr__(self):
        return "Artists: {}, Tracks: {}, Youtubes: {}, Tags: {}, Track To Tags: {}, Events: {}, Tracks ISAM: {}."\
         .format(self.artists, self.tracks, self.yotubes, self.tags, self.tracks_to_tags, self.events, self.tracks_isam)


if __name__ == "__main__":
    mysql_scripts = MysqlScripts('root', 'songs_track')
    mysql_scripts.insert_folder("create_data/files")
    print("------------------------------------- STATS -----------------------------------------")
    print(mysql_scripts)