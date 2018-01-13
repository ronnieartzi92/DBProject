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

            tomorrow = datetime.now().date() + timedelta(days=1)

            add_employee = ("INSERT INTO employees "
                            "(first_name, last_name, hire_date, gender, birth_date) "
                            "VALUES (%s, %s, %s, %s, %s)")
            add_salary = ("INSERT INTO salaries "
                          "(emp_no, salary, from_date, to_date) "
                          "VALUES (%(emp_no)s, %(salary)s, %(from_date)s, %(to_date)s)")

            data_employee = ('Geert', 'Vanderkelen', tomorrow, 'M', date(1977, 6, 14))

            # Insert new employee
            cursor.execute(add_employee, data_employee)
            emp_no = cursor.lastrowid

            # Insert salary information
            data_salary = {
                'emp_no': emp_no,
                'salary': 50000,
                'from_date': tomorrow,
                'to_date': date(9999, 1, 1),
            }
            # cursor.execute(add_salary, data_salary)

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

    @staticmethod
    def main(path):
        with open(path) as fp:
            json_file = json.load(fp)
            artists_list  = json_file['artists']
            for artist_dict in artists_list:
                artist = Artist(artist_dict['name'], artist_dict['description'])
                artist_track_list = artist_dict['tracks']
                artist_event_list = artist_dict['events']

                print("artist:", artist.__dict__)

                for track_dict in artist_track_list:
                    track = Track(track_dict['name'], track_dict['img'], track_dict['lyrics'], track_dict['description'])
                    youtube_dict = track_dict['youtube']
                    youtube = Youtube(youtube_dict['video_id'], youtube_dict['duration'], youtube_dict['date_published'], youtube_dict['description'])
                    tag_list = track_dict['tags']

                    print("\ttrack:", track.__dict__)
                    print("\t\tyoutube:", youtube.__dict__)

                    for tag_str in tag_list:
                        tag = Tag(tag_str)
                        print("\t\ttag:", tag.__dict__)



                for event_dict in artist_event_list:
                    event = Event(event_dict['location'], event_dict['date'], event_dict['uri'])
                    print("\tevent:", event.__dict__)


if __name__ == "__main__":
    # mysql_scripts = MysqlScripts('root', 'fogi')
    # mysql_scripts.connect()
    # MysqlScripts.main('example.json')
    add_employee = ("INSERT INTO employees "
                    "(first_name, last_name, hire_date, gender, birth_date) "
                    "VALUES (%s, %s, %s, %s, %s)")
    print(add_employee)