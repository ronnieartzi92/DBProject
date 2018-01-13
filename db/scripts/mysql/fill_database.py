from __future__ import print_function
from datetime import date, datetime, timedelta
import mysql.connector
import json
from db.entities.entities import *
from mysql.connector import errorcode


class MysqlScripts:
    def __init__(self, user, database):
        self.user = user
        self.database = database

    def connect(self):
        try:
            cnx = mysql.connector.connect(user=self.user, database=self.database)
            cursor = cnx.cursor()

            emp_no = cursor.lastrowid
            db_tag_id = Tag("rock").find_id_by_name(cursor)

            # Make sure data is committed to the database
            cnx.commit()
            cursor.close()
            cnx.close()
        except mysql.connector.Error as err:
          if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
          elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
          else:
            print(err)
        else:
          cnx.close()

    def insert(self):
        cnx = mysql.connector.connect(user=self.user, database=self.database)
        cursor = cnx.cursor()
        b = User("mike@gmail.com", "number2-lastlast", "sahjgjsaa", 1)
        b.insert(cursor)
        emp_no = cursor.lastrowid
        print(emp_no)
        cnx.commit()
        cursor.close()
        cnx.close()

    def insert_artists(self, path):

        # creating connection to db
        cnx = mysql.connector.connect(user=self.user, database=self.database)
        cursor = cnx.cursor()

        # inserting json file to db
        with open(path) as fp:
            json_file = json.load(fp)
            artists_list  = json_file['artists']

            # Artist
            for artist_dict in artists_list:
                artist = Artist(artist_dict['name'], artist_dict['description'])
                artist_track_list = artist_dict['tracks']
                artist_event_list = artist_dict['events']
                artist_id = artist.insert(cursor)

                # Track
                for track_dict in artist_track_list:
                    track = Track(artist_id, track_dict['name'], track_dict['img'], track_dict['lyrics'], track_dict['description'])
                    tag_list = track_dict['tags']
                    youtube_dict = track_dict['youtube']
                    track_id = track.insert(cursor)

                    # Youtube
                    youtube = Youtube(track_id, youtube_dict['video_id'], youtube_dict['duration'], youtube_dict['date_published'], youtube_dict['description'])

                    print("\ttrack:", track.__dict__)
                    print("\t\tyoutube:", youtube.__dict__)

                    # Tag
                    for tag_str in tag_list:
                        tag = Tag(tag_str)
                        tag_id = tag.find_id_by_name(cursor)
                        if tag_id is None: # Tag isn't in DB
                            tag_id = tag.insert()

                        TrackToTag(track_id, tag_id)
                # Event
                for event_dict in artist_event_list:
                    event = Event(event_dict['location'], event_dict['date'], event_dict['uri'])
                    print("\tevent:", event.__dict__)

                # closing resources
                cnx.commit()
                cursor.close()
                cnx.close()



if __name__ == "__main__":
    mysql_scripts = MysqlScripts('root', 'fogi')
    # mysql_scripts.insert()
    # MysqlScripts.insert_artists('example.json')
    mysql_scripts.connect()