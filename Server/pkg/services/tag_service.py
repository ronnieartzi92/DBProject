from ..mysql_service import *
from flask import jsonify


class TagService:

    @staticmethod
    def get_all():
        re = run_get_query("select * from tags")
        return jsonify(re)