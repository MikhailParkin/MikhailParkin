import logging

from flask import Blueprint, render_template, request, redirect, url_for
from sqlalchemy.exc import DatabaseError, IntegrityError
from werkzeug.exceptions import BadRequest, NotFound, InternalServerError

from homework_06.models import db, Author
from homework_06.views.forms.author import AuthorForm

author_app = Blueprint("author_app", __name__)


@author_app.route("/", endpoint="authors")
def list_authors():
    authors = Author.query.order_by(Author.id).all()
    return render_template("authors/list.html", authors=authors)


@author_app.route("/<int:author_id>/", methods=["GET", "POST"], endpoint="details")
def get_author_by_id(author_id: int):
    authors = Author.query.get(author_id)
    form = AuthorForm()
    if request.method == "GET" or not form.validate_on_submit():
        return render_template(
            "authors/author_details.html",
            authors=authors,
            form=form,
        )
    if authors is None:
        raise NotFound(f"Author with id #{author_id} not found!")
    return redirect(url_for("author_app.details", author_id=authors.id))


def save_author(author_name, author_email):
    try:
        db.session.commit()
    except IntegrityError as ex:
        logging.warning("got integrity error with text %s", ex)
        raise BadRequest(f"Could not save author {author_name}, probably name or {author_email} is not unique")
    except DatabaseError:
        db.session.rollback()
        logging.exception("got db error!")
        raise InternalServerError(f"could not save product with name {author_name}!")


@author_app.route("/author_add/", methods=["GET", "POST"], endpoint="add")
def author_add():
    form = AuthorForm()
    if request.method == "GET":
        return render_template("authors/add_author.html", form=form)

    if not form.validate_on_submit():
        return render_template("authors/add_author.html", form=form)

    author = Author(name=form.data["name"], username=form.data["username"], email=form.data["email"])
    db.session.add(author)
    save_author(author.name, author.email)
    return redirect(url_for("author_app.details", author_id=author.id))
