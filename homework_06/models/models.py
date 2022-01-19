from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Text
from .database import db


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


