"""
Домашнее задание №4
Асинхронная работа с сетью и бд

доработайте функцию main, по вызову которой будет выполняться полный цикл программы
(добавьте туда выполнение асинхронной функции async_main):
- создание таблиц (инициализация)
- загрузка пользователей и постов
    - загрузка пользователей и постов должна выполняться конкурентно (параллельно)
      при помощи asyncio.gather (https://docs.python.org/3/library/asyncio-task.html#running-tasks-concurrently)
- добавление пользователей и постов в базу данных
  (используйте полученные из запроса данные, передайте их в функцию для добавления в БД)
- закрытие соединения с БД
"""
import asyncio
from models import engine, User, Post, Base
from jsonplaceholder_requests import fetch_users, fetch_posts
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def add_users_from_json(users: dict):
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        session: AsyncSession
        async with session.begin():
            for user in users:
                user_data = User(name=user['name'],
                                 username=user['username'],
                                 email=user['email'],
                                 website=user['website'])
                session.add(user_data)


async def add_posts_from_json(posts: dict):
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        session: AsyncSession
        async with session.begin():
            for post in posts:
                post_data = Post(user_id=post['userId'],
                                 title=post['title'],
                                 body=post['body'])
                session.add(post_data)


async def async_main():
    await create_tables()
    users, posts = await asyncio.gather(fetch_users(), fetch_posts())
    await add_users_from_json(users)
    await add_posts_from_json(posts)


def main():
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
