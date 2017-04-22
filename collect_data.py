import os
import json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

access_token = os.environ['TWITTER_ACCESS_TOKEN']
access_token_secret = os.environ['TWITTER_ACCESS_TOKEN_SECRET']
consumer_key = os.environ['TWITTER_CONSUMER_KEY']
consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']


class StdOutListener(StreamListener):

    def on_data(self, data):
        tweet = {}
        status = json.loads(data)
        if 'coordinates' in status and status['coordinates']:
            tweet['text'] = status['text']
            tweet['coordinates'] = status['coordinates']
            print(tweet)
        elif 'place' in status and status['place']:
            tweet['text'] = status['text']
            tweet['place'] = status['place']['full_name']
            print(tweet)

        if tweet:
            with open('tweets_with_location.txt','a') as tf:
                tf.write(str(status) + "\n")

        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':

    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    stream.filter(track=['trump', '@realDonalTrump'])
