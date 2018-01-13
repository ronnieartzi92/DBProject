from abc import ABC, abstractmethod

class AbstractTable(ABC):
    @property
    def table_name(self):
        raise NotImplementedError

    @property
    def columns(self):
        raise NotImplementedError

    def num_of_columns(self):
        return self.columns.count(',') + 1

    def create_str_values(self):
        return '(' + '%s, ' * (self.num_of_columns() - 1) + '%s)'

    def insert(self, cursor):
        command = "INSERT INTO %s %s " % (self.table_name, self.columns) + self.create_str_values()
        data = self.__dict__
        return command
        # cursor.execute(add_employee, data_employee)


class User(AbstractTable):
    table_name = 'users'
    columns = "(email, google_id, google_img, is_admin)"

    def __init__(self, email, google_id, google_img, is_admin):
        self.email = email
        self.google_id = google_id
        self.google_img = google_img
        self.is_admin = is_admin


class PlayList(AbstractTable):
    table_name = 'play_lists'
    columns = "(name, date_created)"

    def __init__(self, name, date_created):
        self.name = name
        self.date_created = date_created


class Artist(AbstractTable):
    table_name = 'artists'
    columns = "(name, description)"

    def __init__(self, name, description):
        self.name = name
        self.description = description


class Track(AbstractTable):
    table_name = 'tracks'
    columns = "(name, img, lyrics, description)"

    def __init__(self, name, img, lyrics, description):
        self.name = name
        self.img = img
        self.lyrics = lyrics
        self.description = description


class TrackToTag(AbstractTable):
    table_name = 'tracks_to_tags'
    columns = "(track_id, tag_id)"

    def __init__(self, track_id, tag_id):
        self.track_id = track_id
        self.tag_id = tag_id


class Youtube(AbstractTable):
    table_name = 'youtubes'
    columns = "(video_id, duration, date_published, description)"

    def __init__(self, video_id, duration, date_published, description):
        self.video_id = video_id
        self.duration = duration
        self.date_published = date_published
        self.description = description


class Tag(AbstractTable):
    table_name = 'tags'
    columns = "(name)"

    def __init__(self, name):
        self.name = name


class Event(AbstractTable):
    table_name = 'events'
    columns = "(location, date, uri)"

    def __init__(self, location, date, time, uri):
        self.location = location
        self.date = date
        self.uri = uri

