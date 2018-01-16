from flask import Flask

from auth import auth
from routers.users import users
from routers.playlist_router import playlist_router
from routers.tag_router import tag_router
from routers.artist_router import artist_router
from mysql_service import *

app = Flask(__name__)
app.secret_key = "omri22"


@app.route("/sql")
def hello():
    re = run_and_commit_query(("insert into actor(actor_id,first_name,last_name) values(565,'omro','fdgdf')"))
    for x in re:
        print x.keys()

    return "Hello World!"


@app.route("/sqlGet")
def hello2():
    re = run_get_query(("select * from actor"))
    for x in re:
        print x

    return "Hello World!"


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
    # app.register_blueprint(users)
    app.register_blueprint(playlist_router)
    app.register_blueprint(tag_router)
    app.register_blueprint(artist_router)
    app.run()
