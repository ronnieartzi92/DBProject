from flask import Blueprint, request
from pkg.services.track_service import *
import json

track_router = Blueprint('track', 'track', url_prefix='/track')


@track_router.route("/search", methods=["GET"], strict_slashes=False)
def full_text_search():
    str_to_search = request.args.get("text")
    limit = 10 if request.args.get("limit") is None else int(request.args.get("limit"))
    return TrackService.full_text_search(str_to_search, limit)
