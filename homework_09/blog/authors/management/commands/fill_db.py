from django.core.management.base import BaseCommand

from authors.models import Post
from myauth.models import MyUser

from aiohttp import ClientSession
import asyncio

USERS_DATA_URL = "https://jsonplaceholder.typicode.com/users"
POSTS_DATA_URL = "https://jsonplaceholder.typicode.com/posts"


async def fetch_json(session: ClientSession, url: str):
    async with session.get(url) as response:
        return await response.json()


async def fetch_users():
    async with ClientSession() as session:
        json_data = await fetch_json(session, USERS_DATA_URL)
    return json_data


async def fetch_posts():
    async with ClientSession() as session:
        json_data = await fetch_json(session, POSTS_DATA_URL)
    return json_data


async def test_data():
    users, posts = await asyncio.gather(fetch_users(), fetch_posts())
    return users, posts


def data_json():
    asyncio.set_event_loop(asyncio.SelectorEventLoop())
    users, posts = asyncio.get_event_loop().run_until_complete(test_data())
    return users, posts


class Command(BaseCommand):

    def handle(self, *args, **options):
        users, posts = data_json()
        for user in users:
            first_name = user['name'].split(' ', 1)[0]
            last_name = user['name'].split(' ', 1)[1]
            myuser = MyUser.objects.create_user(user['username'],
                                                user['email'],
                                                user['username'])
            myuser.first_name = first_name
            myuser.last_name = last_name
            myuser.save()
            # MyUser.objects.get_or_create(username=user['username'],
            #                              first_name=first_name,
            #                              last_name=last_name,
            #                              email=user['email'],
            #                              password=user['username'])

        for post in posts:
            Post.objects.get_or_create(title=post['title'], body=post['body'], name_id=post['userId'])
