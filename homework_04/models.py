"""
создайте алхимичный engine
добавьте declarative base (свяжите с engine)
создайте объект Session
добавьте модели User и Post, объявите поля:
для модели User обязательными являются name, username, email
для модели Post обязательными являются user_id, title, body
создайте связи relationship между моделями: User.posts и Post.user

- доработайте модуль `models`:
    - создайте асинхронный алхимичный `engine` (при помощи `create_async_engine`)
    - добавьте `declarative base`
    - создайте объект `Session` на основе класса `AsyncSession`
    - добавьте модели `User` и `Post`, объявите поля:
        - для модели `User` обязательными являются `name`, `username`, `email`
        - для модели `Post` обязательными являются `user_id`, `title`, `body`
        - создайте связи `relationship` между моделями: `User.posts` и `Post.user`
"""

import os
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, declared_attr, InstrumentedAttribute
from sqlalchemy import Column, Integer, String, ForeignKey, Text

PG_CONN_URI = os.environ.get("SQLALCHEMY_PG_CONN_URI") or "postgresql+asyncpg://user:password@localhost/postgres"

engine = create_async_engine(PG_CONN_URI)

Session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base:

    @declared_attr
    def __tablename__(cls):
        return f"blog_app__{cls.__name__.lower()}s"

    id = Column(Integer, primary_key=True)

    def __str__(self):
        attributes = [
            f"{name}={(getattr(self, name))!r}"
            for name, value in vars(self.__class__).items()
            if not name.startswith("_") and isinstance(value, InstrumentedAttribute)
        ]
        return f"{self.__class__.__name__}({', '.join(attributes)})"

    def __repr__(self):
        return str(self)


Base = declarative_base(cls=Base)


class User(Base):
    def __init__(self, id: int, name: str, username: str, email: str):
        self.id = id
        self.name = name
        self.username = username
        self.email = email

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, unique=True)

    posts = relationship("Post", back_populates="user")


class Post(Base):
    def __init__(self, id: int, user_id: int, title: str, body: str):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.body = body

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey(User.id), nullable=False)
    title = Column(String)
    body = Column(Text)

    user = relationship("User", back_populates="post")


