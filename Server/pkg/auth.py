from flask import request
from urllib2 import Request, urlopen, URLError
import json
from mysql_service import *
GOOGLE_CLIENT_ID = "60150906703-els4j53jkve5kd9ijdf70s5l7k40ccsd.apps.googleusercontent.com"


def auth(func):
    def inner_auth():
        if "Authorization" in request.headers:
            id_token = request.headers["Authorization"].split(" ")[1]
            req = Request('https://www.googleapis.com/oauth2/v3/tokeninfo?id_token='+id_token, None, {})
            try:
                res = urlopen(req)
            except URLError:
                return "Unauthorized!", 401

            data = json.load(res)
            if data["aud"] == GOOGLE_CLIENT_ID:
                return func(get_internal_user_id(data))
        return "Unauthorized!", 401
    inner_auth.func_name = func.func_name
    return inner_auth


def get_internal_user_id(google_data):
    query = "select * from users where google_id = "+google_data["sub"]
    result = run_get_query(query)

    if len(result) > 0:
        return result[0]["id"]
    return create_new_user(google_data)


def create_new_user(google_data):
    g_id = google_data["sub"]
    email = google_data["email"]
    img = google_data["picture"]
    is_admin = False

    query = "insert into users(email, google_id, google_img, is_admin) VALUES('{}','{}','{}',{})"
    query = query.format(email, g_id, img, is_admin)

    id = run_and_commit_query(query)
    return id
