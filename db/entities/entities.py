from abc import ABC, abstractmethod


class AbstractTable(ABC):
    @property
    def table_name(self):
        raise NotImplementedError

    def create_str_values(self):
        def num_of_columns(self):
            return self.columns.count(',') + 1
        return '(' + '%s, ' * (self.num_of_columns() - 1) + '%s)'

    def get_columns_values(self):
        keys = tuple(self.__dict__.keys())
        values = tuple([self.__dict__[key] for key in keys])
        return keys, values

    def insert(self, cursor):
        columns, values = self.get_columns_values()
        command = "INSERT INTO %s %s " % (self.table_name, str(columns).replace("'","")) + "VALUES " + '(' + '%s, ' * (len(columns) - 1) + '%s)'
        cursor.execute(command, values)
        return cursor.lastrowid


class User(AbstractTable):
    table_name = 'users'

    def __init__(self, email, google_id, google_img, is_admin):
        self.email = email
        self.google_id = google_id
        self.google_img = google_img
        self.is_admin = is_admin


class PlayList(AbstractTable):
    table_name = 'play_lists'

    def __init__(self, user_id,  name, date_created):
        self.user_id = user_id
        self.name = name
        self.date_created = date_created


class Artist(AbstractTable):
    table_name = 'artists'

    def __init__(self, name, description, img, play_count):
        self.name = name
        self.description = description
        self.img = img
        self.play_count = play_count


class Track(AbstractTable):
    table_name = 'tracks'

    def __init__(self, artist_id, name, album, play_count, img, lyrics, description):
        self.artist_id = artist_id
        self.name = name
        self.album = album
        self.play_count = play_count
        self.img = img
        self.lyrics = lyrics
        self.description = description


class TrackToTag(AbstractTable):
    table_name = 'tracks_to_tags'

    def __init__(self, track_id, tag_id):
        self.track_id = track_id
        self.tag_id = tag_id


class Youtube(AbstractTable):
    table_name = 'youtubes'

    def __init__(self, track_id, url, duration, date_published, description):
        self.track_id = track_id
        self.url = url
        self.duration = duration
        self.date_published = date_published
        self.description = description


class Tag(AbstractTable):
    table_name = 'tags'

    def __init__(self, name):
        self.name = name

    def find_id_by_name(self, cursor):
        command = "SELECT id FROM %s WHERE tags.name='%s'" % (self.table_name, self.name)
        cursor.execute(command)
        row = cursor.fetchone()
        return None if row is None else row[0]


class Event(AbstractTable):
    table_name = 'events'

    def __init__(self, artist_id, location, date, url, description, title):
        self.artist_id = artist_id
        self.location = location
        self.date = date
        self.url = url
        self.description = description
        self.title = title

