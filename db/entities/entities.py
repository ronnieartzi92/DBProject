
class User:
    table_name = 'users'
    columns = "(email, google_id, google_img, is_admin)"

    def __init__(self, email, google_id, google_img, is_admin):
        self.email = email
        self.google_id = google_id
        self.google_img = google_img
        self.is_admin = is_admin


class PlayList:
    table_name = 'play_lists'
    columns = "(name, date_created)"

    def __init__(self, name, date_created):
        self.name = name
        self.date_created = date_created


class Artist:
    table_name = 'artists'
    columns = "(name, description)"

    def __init__(self, name, description):
        self.name = name
        self.description = description


class Track:
    table_name = 'tracks'
    columns = "(name, img, lyrics, description)"

    def __init__(self, name, img, lyrics, description):
        self.name = name
        self.img = img
        self.lyrics = lyrics
        self.description = description


class TrackToTag:
    table_name = 'tracks_to_tags'
    columns = "(track_id, tag_id)"

    def __init__(self, track_id, tag_id):
        self.track_id = track_id
        self.tag_id = tag_id


class Youtube:
    table_name = 'youtubes'
    columns = "(video_id, duration, date_published, description)"

    def __init__(self, video_id, duration, date_published, description):
        self.video_id = video_id
        self.duration = duration
        self.date_published = date_published
        self.description = description


class Tag:
    table_name = 'tags'
    columns = "(name)"

    def __init__(self, name):
        self.name = name


class Event:
    table_name = 'events'
    columns = "(location, date, uri)"

    def __init__(self, location, date, time, uri):
        self.location = location
        self.date = date
        self.uri = uri

