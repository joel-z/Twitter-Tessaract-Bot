from time import sleep

from src.conf.pumped_coins import PumpedCoins
from src.settings import coin_of_the_day_filter, sell_order_multiplier
from src.twitter import get_user_timeline
from src.conf.last_tweet_id import LastTweetID
from src.conf.bittrex_coins import coins, coins_abbr
from src.bittrex import buy, sell

from PIL import Image
from pytesseract import image_to_string
import urllib.request

def main():
    mcafee_tid = 961445378
    tweets = get_user_timeline(mcafee_tid, LastTweetID.get()).json()

    if len(tweets) != 0:
        max_id_tweet = max(tweets, key=lambda tweet: tweet['id'])
        last_tweet_id = max_id_tweet['id_str']
        LastTweetID.update(last_tweet_id)

    while True:
        # API Rate limits you to check user timeline only once per second (900 per 15 mins)
        sleep(1)

        done = False
        bought_coin = None

        tweets = get_user_timeline(mcafee_tid, LastTweetID.get()).json()
        if len(tweets) == 0:
            continue
        else:
            print("RECEIVED {0} tweets".format(len(tweets)))
        max_id_tweet = max(tweets, key=lambda tweet: tweet['id'])
        last_tweet_id = max_id_tweet['id_str']

        for tweet in tweets:
            tweet_text = tweet['text']

            if 'entities' in tweet and 'media' in tweet['entities']:
                for i, media in enumerate(tweet['entities']['media']):
                    if 'media_url' in media:
                        image_url = media['media_url'] 
                        out_name = str(tweet['id']) + str(i) + "." + str(image_url.split('.')[-1])
                        urllib.request.urlretrieve(image_url, out_name)
                        tweet_text += ' ' + image_to_string(Image.open(out_name))

            tweet_text = tweet_text.upper()

            print(tweet_text)

            # Filter for "coin of the day"
            if coin_of_the_day_filter is True and "COIN OF THE DAY" not in tweet_text:
                continue

            # Check for full coin names
            for coin_fullname in coins.keys():
                coin_name_up = coin_fullname.upper()
                if (coin_name_up + " ") in tweet_text or (" " + coin_name_up) in tweet_text:
                    if coin_name_up == "ION":  # This coin has a really short name... dangerous
                        if (" " + coin_name_up + " ") not in tweet_text:
                            continue
                    if coins[coin_fullname] in PumpedCoins.pumped_coins:
                        print("Mr. McAfee just tweeted about an already-pumped coin {0}".format(coins[coin_fullname]))
                        continue
                    done = True
                    bought_coin = coins[coin_fullname]
                    break
            if done:
                break
        if done:
            bid_price = buy(bought_coin)
            sell(bought_coin, bid_price * sell_order_multiplier)
            PumpedCoins.add(bought_coin)

        LastTweetID.update(last_tweet_id)


