# Built-In Modules

# external Modules
from flask import Blueprint, current_app, request, session

from autonomous import log
from autonomous.auth import auth_required

api_page = Blueprint("api", __name__)


@api_page.route("/", methods=("GET",))
def index():
    return {}


@api_page.route("/protected", methods=("GET",))
@auth_required
def protected():
    log(session["user"])
    log(current_app)
    session["user"] = None
    return {**session}
