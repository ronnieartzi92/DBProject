from __future__ import print_function
import json
import os

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
                try:
                    artist_id = artist.insert(cursor)
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
                    except Exception as e:
                        MysqlScripts.print_entity(e, track)
                        continue

                    # Youtube
                    youtube = Youtube(track_id, youtube_dict['video_id'], youtube_dict['duration'], youtube_dict['date_published'], youtube_dict['description'])
                    try:
                        youtube.insert(cursor)
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
                            except Exception as e:
                                MysqlScripts.print_entity(e, tag)
                                continue

                        # TrackToTag
                        track_to_tag = TrackToTag(track_id, tag_id)
                        try:
                            track_to_tag.insert(cursor)
                        except Exception as e:
                            MysqlScripts.print_entity(e, track_to_tag)
                            continue

                # Event
                for event_dict in artist_event_list:
                    event = Event(artist_id, event_dict['country'], event_dict['city'], event_dict['venue'], event_dict['date'], event_dict['url'], event_dict['description'], event_dict['title'], event_dict['img'])
                    try:
                        event.insert(cursor)
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
        print("-------------- Exception---------------------")
        print(exp)
        print("class:", obj.__class__)
        for key in obj.__dict__:
            print(key + ":", obj.__dict__[key])
        print("--------------------------------------------")

    def stam(self, obj):
        cnx = mysql.connector.connect(user=self.user, database=self.database)
        cursor = cnx.cursor()
        try:
            obj.insert(cursor)
        except Exception as e:
            try:
                MysqlScripts.print_entity(e, obj)
            except Exception as e:
                print("############## failed printing all object fields...... ################")
        # closing resources
        cnx.commit()
        cursor.close()
        cnx.close()


if __name__ == "__main__":
    # d = {"description": "\u201cCloser\u201d is a millennial romance anthem that celebrates youth and heartbreak. It features vocals from singer-songwriter Halsey and Chainsmokers member Andrew Taggart, marking the first time The Chainsmokers sung on their own track and the first time they\u2019ve collaborated with Halsey.\n\nOn Twitter, the duo wrote about the meaning of the song:\n\nThis song is dedicated to anyone that hooked up with their EX and right after remember all the reasons why they broke up.\n\n\u201cCloser\u201d was premiered at Bonnaroo by Halsey and she later confirmed its release on her Instagram:\n\n\"You heard it tonight. My phone hasn\u2019t had service in 2 days, bonnaroo but I\u2019m pullin enough juice to inform you that @thechainsmokers and I have a BRAND NEW SONG coming out soon. Those of you who got to witness it tonight, lucky you.\nHalsey also teased the track on Twitter a week prior to the release by releasing a cropped version of the photo featured the single\u2019s art. <a href=\"http://www.last.fm/music/The+Chainsmokers/_/Closer\">Read more on Last.fm</a>. User-contributed text is available under the Creative Commons By-SA License; additional terms may apply."}
    # string = "\ud83d\udc8b\ud83d\udc8b\ud83d\udc8b\"\n"
    # track = Track(1, "mike", "dumb", 1223, "img", "lyrics", d["description"])
    # mysql_scripts.stam(track)
    # print(string)

    mysql_scripts = MysqlScripts('root', 'songs_track')
    mysql_scripts.insert_folder("create_data/files")
