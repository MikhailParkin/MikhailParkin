from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Text
from .database import db

from .request_json import data_json
from sqlalchemy.exc import DatabaseError


class Author(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, default="", server_default="")
    username = Column(String, nullable=False, unique=True)
    email = Column(String, unique=True)
    website = Column(String)

    posts = relationship("Post", back_populates="author")


class Post(db.Model):
    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey(Author.id), nullable=False)
    title = Column(String)
    body = Column(Text)

    author = relationship("Author", back_populates="posts")


def add_test_data():

    users, posts = data_json()

    for user in users:
        user_data = Author(name=user['name'],
                           username=user['username'],
                           email=user['email'],
                           website=user['website'])
        db.session.add(user_data)

    for post in posts:
        post_data = Post(user_id=post['userId'],
                         title=post['title'],
                         body=post['body'])
        db.session.add(post_data)

    try:
        db.session.commit()

    except DatabaseError:
        db.session.rollback()
