from flask import Blueprint, request
from pkg.services.playlist_service import *
from pkg.auth import auth
import json

playlist_router = Blueprint('playlist', 'playlist', url_prefix='/playlist')


@playlist_router.route("/", methods=["POST"],strict_slashes=False)
@auth
def create_playlist(user_id):
    data = request.data
    playlist = json.loads(data)
    return PlaylistService.create_playlist(user_id, playlist)


@playlist_router.route("/", methods=["GET"],strict_slashes=False)
@auth
def get_playlist(user_id):
    if request.args.get("id") is not None:
        return PlaylistService.get_playlist_by_id(1, request.args.get("id"))
    else:
        return PlaylistService.get_all(user_id)


@playlist_router.route("/tags", methods=["POST"],strict_slashes=False)
def add_tags_to_playlist():
    data = request.data
    tags = json.loads(data)
    return PlaylistService.add_tags_to_playlist(request.args.get("id"), tags["tags"])
