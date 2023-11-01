# Built-In Modules

# external Modules
from flask import Blueprint, render_template, request, session

from autonomous import log
from autonomous.auth import auth_required

index_page = Blueprint("index", __name__)


@index_page.route("/", methods=("GET",))
def index():
    return render_template("index.html")


@index_page.route(
    "/protected",
    methods=(
        "GET",
        "POST",
    ),
)
@auth_required
def protected():
    log(session["user"])
    session["user"] = None
    return render_template("index.html")


@index_page.route("/add", methods=("POST",))
def add():
    return {"result": "success"}


@index_page.route("/update", methods=("POST",))
def updates():
    return "updated"


@index_page.route("/delete", methods=("POST",))
def delete():
    return "deleted"
