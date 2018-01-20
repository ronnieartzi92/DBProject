from flask import Flask

import sys
sys.path.append('.')
sys.path.append('../')

from auth import auth
from routers.playlist_router import playlist_router
from routers.tag_router import tag_router
from routers.artist_router import artist_router
from routers.track_router import track_router

app = Flask(__name__)
app.secret_key = "omri22"


@app.route('/')
@auth
def index(user_id):
    return "OK! "+str(user_id)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', '*')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

if __name__ == "__main__":
    app.register_blueprint(playlist_router)
    app.register_blueprint(tag_router)
    app.register_blueprint(artist_router)
    app.register_blueprint(track_router)
    app.run()
