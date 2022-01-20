import logging

from flask import Blueprint, render_template, request, redirect, url_for
from sqlalchemy.exc import DatabaseError, IntegrityError
from werkzeug.exceptions import BadRequest, NotFound, InternalServerError

from homework_06.models import db, Author

author_app = Blueprint("author_app", __name__)


@author_app.route("/", endpoint="authors")
def list_authors():
    authors = Author.query.order_by(Author.id).all()
    return render_template("authors/list.html", authors=authors)


@author_app.route("/<int:author_id>/", endpoint="details")
def get_author_by_id(author_id: int):
    authors = Author.query.get(author_id)
    if authors is None:
        raise NotFound(f"Author with id #{author_id} not found!")
    return redirect(url_for("author_app.details", author_id=authors.id))


@author_app.route("/author_add/", endpoint="add")
def author_add():
    pass