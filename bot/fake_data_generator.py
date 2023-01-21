import random

from faker import Faker


def generate_users_data(max_users: int) -> list[dict]:
    """Generates list of data for user creation"""
    fake = Faker()
    list_of_users = list()
    for _ in range(max_users):
        user = dict()
        user['first_name'] = fake.first_name()
        user['last_name'] = fake.last_name()
        user['email'] = fake.email()
        user['password'] = fake.password()
        user['username'] = fake.user_name()
        list_of_users.append(user)
    return list_of_users


def generate_posts_data(max_posts: int) -> list[dict]:
    """Generates list of dicts with post data"""
    fake = Faker()
    list_of_posts = list()
    for _ in range(random.randrange(1, max_posts)):
        post = dict()
        post['title'] = fake.name()
        list_of_posts.append(post)
    return list_of_posts
