import json

import aiohttp
import asyncio

from fake_data_generator import generate_posts_data, generate_users_data

BASE_URL = 'http://127.0.0.1:80'

with open('bot_config.json', 'r') as config_file:
    config_data = json.load(config_file)

print(config_data)


async def signup_exact_amount_of_users(users_amount: int = config_data.get('number_of_users')) -> list:
    auth_token_list = list()
    users_data = generate_users_data(users_amount)
    for user in users_data:
        async with aiohttp.ClientSession(base_url=BASE_URL) as session:
            async with session.post(
                    '/auth/sign-up',
                    json=user, headers={'content-type': 'application/json'}) as response:
                auth_token = await response.json()
                auth_token = f'bearer {auth_token["access_token"]}'
                auth_token_list.append(auth_token)
    return auth_token_list


async def create_exact_amount_of_posts(post_data: dict, user_credential: str) -> dict:
    async with aiohttp.ClientSession(base_url=BASE_URL) as session:
        print(session.headers)
        async with session.post('/posts/create', json=post_data,
                                headers={"WWW-Authenticate": f'',
                                         "Authorization": user_credential,
                                         "content": 'application/json',
                                         'accept': '*/*',
                                         }) as response:
            print(response.raw_headers)
            data = await response.read()
            new_post = json.loads(data)
        return new_post


async def main(max_posts: int = config_data.get('max_posts_per_user')):
    posts = await asyncio.gather(*[
        asyncio.ensure_future(create_exact_amount_of_posts(post_data, user_credential))
        for user_credential in await signup_exact_amount_of_users()
        for post_data in generate_posts_data(max_posts)
    ])
    return posts


if __name__ == '__main__':
    asyncio.run(main())
