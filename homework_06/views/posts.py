import logging

from flask import Blueprint, render_template, request, redirect, url_for
from sqlalchemy.exc import DatabaseError, IntegrityError
from werkzeug.exceptions import BadRequest, NotFound, InternalServerError

from homework_06.models import db, Post, Author

post_app = Blueprint("post_app", __name__)


@post_app.route("/", endpoint="posts")
def list_authors():
    posts = Post.query.all()
    return render_template("posts/list_posts.html", posts=posts)


@post_app.route("/<int:author_id>/", endpoint="details_post")
def get_author_by_id(author_id: int):
    posts = Post.query.join(Author).filter_by(id=author_id).all()
    author = Author.query.get(author_id)
    return render_template("posts/post_detail.html", posts=posts, author=author)


@post_app.route("/author_add/", endpoint="add")
def author_add():
    pass
