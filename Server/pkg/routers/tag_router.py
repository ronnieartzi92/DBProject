from flask import Blueprint, request
from pkg.services.tag_service import *

tag_router = Blueprint('tag', 'tag', url_prefix='/tag')


@tag_router.route("/", methods=["GET"],strict_slashes=False)
def get_all_tags():
    return TagService.get_all()

