import json
import random
import os.path
import sys
from typing import List

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from django.db import transaction
from faker import Faker

from users.models import Company
from posts.models import Post
from posts.constants import REACTION_STATUSES


User = get_user_model()
fake = Faker()

required_fields = {
    'user_number',
    'max_posts_per_user',
    'max_reactions_per_user'
}


class Command(BaseCommand):
    help = 'read config and create entities in db'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **options):
        path = options.get('path')
        if not path:
            self.stdout.write('Please provide a valid --path argument.')
            sys.exit(1)
        elif not os.path.isfile(path):
            self.stdout.write(f'Can\'t find the file at provided path {path}.')
            sys.exit(1)

        with open(path) as f:
            data = json.load(f)

        if not required_fields.issubset(set(data.keys())):
            self.stdout.write(
                'A valid config must include the following fields: '
                f'{", ".join(required_fields)}')

        with transaction.atomic():
            users = create_users(data['user_number'])
            for u in users:
                password = fake.password(
                    length=random.randint(10, 20),
                    special_chars=True,
                    digits=True,
                    upper_case=True,
                    lower_case=True
                )
                u.set_password(password)
                u.save()

            posts = create_posts(users, data['max_posts_per_user'])
            Post.objects.bulk_create(posts)
            react_to_posts(users, posts, data['max_reactions_per_user'])


def create_users(user_number: int) -> List[User]:
    users = []
    for _ in range(user_number):
        user = {
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'email': fake.ascii_free_email(),
        }

        # add company to some users
        if random.randint(0, 1) == 1:
            company_name = fake.company()
            company = Company(**{
                'name': company_name,
                'legal_name': company_name,
                'location': fake.address(),
                'description':  ' '.join(fake.sentences()),
                'domain': fake.domain_name(),
            })
            company.save()
            user['company'] = company
        users.append(User(**user))

    return users


def create_posts(users: List[User], posts_per_user: int) -> List[Post]:
    posts = []
    for user in users:
        for _ in range(random.randint(0, posts_per_user)):
            posts.append(
                Post(**{
                    'user': user,
                    'title': ' '.join(fake.words()).capitalize(),
                    'content': fake.text(max_nb_chars=1000),
                }))

    return posts


def react_to_posts(
        users: List[User],
        posts: List[Post],
        max_reactions_per_user: int
) -> None:
    for user in users:
        reactions = [int(random.choice(REACTION_STATUSES.values()))
                     for _ in range(random.randint(0, max_reactions_per_user))]
        likes = reactions.count(REACTION_STATUSES.LIKE.value)
        dislikes = reactions.count(REACTION_STATUSES.DISLIKE.value)
        selection_len = min(len(posts), likes + dislikes)
        selection = (random.sample(posts, selection_len)
                     if selection_len < len(posts) else posts)
        for post in selection:
            if likes:
                post.upvoted_by.add(user)
                likes -= 1
            elif dislikes:
                post.downvoted_by.add(user)
                dislikes -= 1
