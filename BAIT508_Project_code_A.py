# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 00:18:55 2017

@author: Howard
"""

# from twython package import TwythonStreamer module
from twython import TwythonStreamer
import sys
import json
 
# global variable to store tweets
tweets = []
 
# we are inheriting from TwythonStreamer class
class MyStreamer(TwythonStreamer):
    '''our own subclass of TwythonStreamer'''
 
    # overriding
    def on_success(self, data):
        # check if the received tweet dictionary is in English
        if 'lang' in data and data['lang'] == 'en':
            tweets.append(data)
            print('received tweet #', len(tweets), data['text'][:200])
 
        # if we have enough tweets, store it into JSON file and disconnect API
        if len(tweets) >= 100:
            self.store_json()
 
    # overriding
    def on_error(self, status_code, data):
        print(status_code, data)
        self.disconnect()
 
    # our new method to store tweets into JSON file
    def store_json(self):
        with open('tweet_stream_{}_{}_{}.json'.format(keyword, len(tweets),times), 'w') as f:
            json.dump(tweets, f, indent=4)
            self.disconnect()
 
# check if we are running this code as top-level module
if __name__ == '__main__':
 
    #with open('your_twitter_credentials.json', 'r') as f:
    with open('F:\BAIT508\Credential.json', 'r') as f:
        credentials = json.load(f)
 
    # create your own app to get consumer key and secret
    CONSUMER_KEY = credentials['CONSUMER_KEY']
    CONSUMER_SECRET = credentials['CONSUMER_SECRET']
    ACCESS_TOKEN = credentials['ACCESS_TOKEN']
    ACCESS_TOKEN_SECRET = credentials['ACCESS_TOKEN_SECRET']
 
    # Twitter Streaming API needs all four credentials
    stream = MyStreamer(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
 
    # we will get system arguments to get keyword
    # you can run this code by:
    # python 3_test_twitter_stream.py MyKeyword
    if len(sys.argv) > 1:
        keyword = sys.argv[1]
    else:
        keyword = 'Cannabis'
 
    # Github Code: https://github.com/ryanmcgrath/twython/blob/master/twython/streaming/types.py
    # Accepted parameters: https://developer.twitter.com/en/docs/tweets/filter-realtime/api-reference/post-statuses-filter
    for times in range(0,100):
        stream.statuses.filter(track=keyword)
        tweets = []

#Code source: UBC BAIT508 Professor Gene Lee