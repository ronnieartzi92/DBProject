class User:
    def __init__(self, email, google_id, google_img, is_admin):
        self.email = email
        self.google_id = google_id
        self.google_img = google_img
        self.is_admin = is_admin


class PlayList:
    def __init__(self, name, date_created):
        self.name = name
        self.date_created = date_created


class Artist:
    def __init__(self, name, description):
        self.name = name
        self.description = description


class Track:
    def __init__(self, name, img, lyrics, description):
        self.name = name
        self.img = img
        self.lyrics = lyrics
        self.description = description


class TrackToTag:
    def __init__(self, track_id, tag_id):
        self.track_id = track_id
        self.tag_id = tag_id


class Youtube:
    def __init__(self, video_id, duration, date_published, description):
        self.video_id = video_id
        self.duration = duration
        self.date_published = date_published
        self.description = description


class Tag:
    def __init__(self, name):
        self.name = name


class Event:
    def __init__(self, location, date, time, uri):
        self.location = location
        self.date = date
        self.time = time
        self.uri = uri

