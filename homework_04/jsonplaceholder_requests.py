"""
создайте асинхронные функции для выполнения запросов к ресурсам (используйте aiohttp)
- доработайте модуль `jsonplaceholder_requests`:
    - установите значения в константы `USERS_DATA_URL` и `POSTS_DATA_URL` (ресурсы нужно взять отсюда https://jsonplaceholder.typicode.com/)
    - создайте асинхронные функции для выполнения запросов к данным ресурсам (используйте `aiohttp`)
    - рекомендуется добавить базовые функции для запросов, которые будут переиспользованы (например `fetch_json`)

"""
from aiohttp import ClientSession
import asyncio
# import logging
#
# DEFAULT_FORMAT = "%(asctime)s %(levelname)-8s [%(name)-8s] (%(filename)s:%(funcName)s:%(lineno)d) %(message)s"
#
# logging.basicConfig(format=DEFAULT_FORMAT, level=logging.DEBUG)
#
# log = logging.getLogger(__name__)

USERS_DATA_URL = "https://jsonplaceholder.typicode.com/users"
POSTS_DATA_URL = "https://jsonplaceholder.typicode.com/posts"


async def fetch_json(session: ClientSession, url: str):
    async with session.get(url) as response:
        return await response.json()


async def fetch_users():
    # log.info(f"Fetch users from {USERS_DATA_URL}")
    async with ClientSession() as session:
        json_data = await fetch_json(session, USERS_DATA_URL)
    # log.info(f"Fetch json from {USERS_DATA_URL}: {json_data}")
    return json_data


async def fetch_posts():
    # log.info(f"Fetch posts from {POSTS_DATA_URL}")
    async with ClientSession() as session:
        json_data = await fetch_json(session, POSTS_DATA_URL)
    # log.info(f"Fetch json from {POSTS_DATA_URL}: {json_data}")
    return json_data


def main():
    asyncio.run(fetch_users())
    asyncio.run(fetch_posts())


if __name__ == '__main__':
    main()
