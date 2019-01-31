import requests
from requests_oauthlib import OAuth1

from src.settings import TwitterAuth


def generate_twitter_oauth1():
    return OAuth1(
        TwitterAuth.consumer_key,
        TwitterAuth.consumer_secret,
        TwitterAuth.access_token,
        TwitterAuth.access_token_secret
    )


oauth1 = generate_twitter_oauth1()


def get_user_timeline(user_id, since_id):
    url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
    params = {
        'user_id': user_id,
        'count': 200,
        'trim_user': False,
        'include_entities': True,
        'since_id': since_id,
        'include_rts': False
    }
    tweets = requests.get(url=url, auth=oauth1, params=params)
    return tweets
