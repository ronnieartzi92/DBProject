from flask import Flask, send_file

import sys
sys.path.append('.')
sys.path.append('../')

from auth import auth
from routers.playlist_router import playlist_router
from routers.tag_router import tag_router
from routers.artist_router import artist_router
from routers.track_router import track_router

app = Flask(__name__, static_url_path='/static')
app.secret_key = "omri22"


@app.route('/static', strict_slashes=False)
def index():
    return app.send_static_file('index.html')


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', '*')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

if __name__ == "__main__":
    if len(sys.argv) != 3:
        host = "0.0.0.0"
        port = 5000
    else:
        host = sys.argv[1]
        port = int(sys.argv[2])
    app.register_blueprint(playlist_router)
    app.register_blueprint(tag_router)
    app.register_blueprint(artist_router)
    app.register_blueprint(track_router)
    app.run(host=host, port=port)
