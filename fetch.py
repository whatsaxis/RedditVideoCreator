"""
Raw data fetching & processing
"""

import json
import requests

from helpers import listify


def get_json(post_id: str = None):
    """Function to fetch Reddit JSON data."""

    # From file
    if post_id is None:

        with open('data.json', 'r') as f:
            return json.loads(f.read())

    # By request
    return requests\
        .get(
            f'https://reddit.com/{ post_id }.json',
            headers={
                'User-agent': f'reddit-video-creator-bot-{ hash(42) }'
            }
        )\
        .json()


def get_post(data) -> dict:
    """Function to extract post data."""

    data = data[0]['data']['children'][0]['data']

    return {
        'subreddit': data['subreddit'],

        'author': data['author'],

        'title': data['title'],
        'over_18': data['over_18'],

        'net_votes': data['score'],
        'upvotes': data['ups'],
        'downvotes': data['downs']
    }


@listify
def get_comments(data) -> list:
    """Function to extract top level comment data."""

    comments = data[1]['data']['children']

    # NOTE: We slice last comment as it is a data field

    for c in comments[:-1]:
        c_data = c['data']

        yield {
            'author': c_data['author'],

            'body': c_data['body'],
            'body_html': c_data['body_html'],

            'net_votes': c_data['score'],
            'upvotes': c_data['ups'],
            'downvotes': c_data['downs']
        }
