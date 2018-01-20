from flask import Blueprint, request
from pkg.services.track_service import *
import json

track_router = Blueprint('track', 'track', url_prefix='/track')


@track_router.route("/search", methods=["GET"], strict_slashes=False)
def full_text_search():
    str_to_search = request.args.get("text")
    limit = 10 if request.args.get("limit") is None else int(request.args.get("limit"))
    return TrackService.full_text_search(str_to_search, limit)


@track_router.route("/concert_tour", methods=["GET"], strict_slashes=False)
def concert_tour():
    limit = 10 if request.args.get("limit") is None else int(request.args.get("limit"))
    return TrackService.concert_tour(limit)


@track_router.route("/artist_on_fire", methods=["GET"], strict_slashes=False)
def artist_on_fire():
    limit = 10 if request.args.get("limit") is None else int(request.args.get("limit"))
    return TrackService.artist_on_fire(limit)
