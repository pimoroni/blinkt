#!/usr/bin/env python

import time
from blinkt import set_pixel, show

try:
    from tweepy import Stream, OAuthHandler
    from tweepy.streaming import StreamListener
except ImportError:
    exit("This library requires the tweepy module\nInstall with: sudo pip install tweepy")

ckey = '' # Consumer key
csecret = '' # Consumer secret
atoken = '' # Access token
asecret = '' # Access secret

class listener(StreamListener):
    def on_data(self, data):
        blink_blinkt()
        return True

    def on_error(self, status):
        print status

def blink_blinkt():
    for i in range(3):
        for j in range(8):
            set_pixel(j, 255, 0, 0)
        show()
        time.sleep(0.1)
        for j in range(8):
            set_pixel(j, 0, 0, 0)
        show()
        time.sleep(0.2)

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterstream = Stream(auth, listener())
twitterstream.filter(track=['#INSERTHASHTAGHERE'])
