from flask import Blueprint, request, session

from pkg.auth import auth

users = Blueprint('users', 'users', url_prefix='/users')


@users.route("/hello")
def hello():
    user = request.args.get('user')
    session["user"] = user
    return "Hello USER!"


@users.route("/helloGet")
@auth
def hello2(user_id):
    return "Hello "+session["user"]

