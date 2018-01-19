from ..mysql_service import *
from flask import jsonify


class PlaylistService:

    @staticmethod
    def get_playlist_by_id(user_id, playlist_id, to_jsonify=True):
        playlists = run_get_query(("select * from play_lists where id = "+str(playlist_id)))
        if len(playlists) == 0:
            raise Exception("Playlist with id "+str(playlist_id)+" wasn't found!")

        songs_query = """
            select tracks.artist_id, youtubes.duration,
            tracks.id, tracks.img, tracks.track_name, tracks.play_count, youtubes.video_id, artists.artist_name as 'artist_name'
            from tracks_to_play_lists, tracks, youtubes, artists
            where play_list_id ="""+playlist_id+"""
            and tracks_to_play_lists.track_id = tracks.id
            and tracks.id = youtubes.track_id
            and tracks.artist_id = artists.id
        """

        songs = run_get_query(songs_query)
        playlists[0]["songs"] = songs
        if to_jsonify:
            return jsonify(playlists[0])
        return playlists[0]

    @staticmethod
    def get_all(user_id):
        playlists = run_get_query(("select * from play_lists where user_id = " + str(user_id)))
        return jsonify(playlists)

    @staticmethod
    def create_playlist(user_id, playlist):
        id = run_and_commit_query("insert into play_lists(play_list_name,user_id) VALUES('{}',{})".format(playlist["name"], user_id))

        base_query = "insert into tracks_to_play_lists(play_list_id, track_id,track_position) VALUES({},{},{})"
        for i in range(len(playlist['songs'])):
            query = base_query.format(id, playlist["songs"][i], i+1)
            run_and_commit_query(query)

        return jsonify(id)

    @staticmethod
    def add_tags_to_playlist(playlist_id,tags):
        playlist = PlaylistService.get_playlist_by_id(0, playlist_id, to_jsonify=False)
        for tag in tags:
            re = run_get_query("select * from tags where tag_name = '"+tag+"'")
            if len(re) > 0:
                id = re[0]["id"]
            else:
                id = run_and_commit_query("insert into tags(tag_name) VALUES ('"+tag+"')")
            for song in playlist["songs"]:
                run_and_commit_query("insert into tracks_to_tags(track_id,tag_id) VALUES({},{})".format(song["id"],id))
        return jsonify(True)