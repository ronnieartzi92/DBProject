from abc import ABC


class AbstractTable(ABC):
    @property
    def table_name(self):
        raise NotImplementedError

    def get_columns_values(self):
        keys = tuple(self.__dict__.keys())
        values = tuple([self.__dict__[key] for key in keys])
        return keys, values

    def insert(self, cursor):
        columns, values = self.get_columns_values()
        command = "INSERT INTO %s %s " % (self.table_name, str(columns).replace("'", "").replace(",)", ")")) + "VALUES " + '(' + '%s, ' * (len(columns) - 1) + '%s)'
        cursor.execute(command, values)
        return cursor.lastrowid


class User(AbstractTable):
    table_name = 'users'

    def __init__(self, email, google_id, google_img, is_admin):
        self.email = email.lower()
        self.google_id = google_id.lower()
        self.google_img = google_img.lower()
        self.is_admin = is_admin


class PlayList(AbstractTable):
    table_name = 'play_lists'

    def __init__(self, user_id, play_list_name, date_created):
        self.user_id = user_id
        self.play_list_name = play_list_name
        self.date_created = date_created


class Artist(AbstractTable):
    table_name = 'artists'

    def __init__(self, artist_name, description, img, play_count):
        self.artist_name = artist_name.title()
        self.description = description
        self.img = img
        self.play_count = play_count


class Track(AbstractTable):
    table_name = 'tracks'

    def __init__(self, artist_id, track_name, album, play_count, img, lyrics, description):
        self.artist_id = artist_id
        self.track_name = track_name.title()
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


class TrackToPlayList(AbstractTable):
    table_name = 'tracks_to_play_lists'

    def __init__(self, play_list_id, track_id, track_position):
        self.play_list_id = play_list_id
        self.track_id = track_id
        self.track_position = track_position


class Youtube(AbstractTable):
    table_name = 'youtubes'

    def __init__(self, track_id, video_id, duration, date_published, description):
        self.track_id = track_id
        self.video_id = video_id
        self.duration = duration
        self.date_published = date_published
        self.description = description


class Tag(AbstractTable):
    table_name = 'tags'

    def __init__(self, tag_name):
        self.tag_name = tag_name.replace('"', "'").lower()

    def find_id_by_name(self, cursor):
        command = 'SELECT id FROM %s WHERE tags.tag_name="%s"' % (self.table_name, self.tag_name)
        cursor.execute(command)
        row = cursor.fetchone()
        return None if row is None else row[0]


class Event(AbstractTable):
    table_name = 'events'

    def __init__(self, artist_id, country, city, venue, date, url, title, img):
        self.artist_id = artist_id
        self.country = country
        self.city = city
        self.venue = venue
        self.date = date
        self.url = url
        self.title = title
        self.img = img
