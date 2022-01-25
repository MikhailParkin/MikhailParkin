import logging

from flask import Blueprint, render_template, request, redirect, url_for
from sqlalchemy.exc import DatabaseError, IntegrityError
from werkzeug.exceptions import BadRequest, NotFound, InternalServerError
from views.forms.author import PostForm

from models import db, Post, Author

post_app = Blueprint("post_app", __name__)


@post_app.route("/", endpoint="posts")
def list_authors():
    posts = Post.query.join(Author).all()
    return render_template("posts/list_posts.html", posts=posts)


@post_app.route("/<int:author_id>/", endpoint="details_post")
def get_author_by_id(author_id: int):
    posts = Post.query.join(Author).filter_by(id=author_id).all()
    return render_template("posts/post_detail.html", posts=posts)


@post_app.route("/body/<int:post_id>/", endpoint="post_body")
def get_post_by_id(post_id: int):
    post = Post.query.get(post_id)
    author = Author.query.get(post.user_id)
    return render_template("posts/post_body.html", post=post, author=author)


def save_post(title):
    try:
        db.session.commit()
    except DatabaseError:
        db.session.rollback()
        logging.exception("got db error!")
        raise InternalServerError(f"could not save post with title {title}!")


@post_app.route("/post_add/", methods=["GET", "POST"], endpoint="add")
def author_add():
    form = PostForm()
    if request.method == "GET":
        authors = Author.query.order_by(Author.id).all()
        return render_template("posts/add_rec.html", authors=authors, form=form)

    if not form.validate_on_submit():
        return render_template("posts/add_rec.html", form=form)
    user = form.data['user_id']
    user_id = user.id
    post = Post(user_id=user_id, title=form.data["title"], body=form.data["body"])
    db.session.add(post)
    save_post(post.title)
    return redirect(url_for("post_app.post_body", post_id=post.id))
