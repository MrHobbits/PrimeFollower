# tweepy-bots/bots/config.py
import tweepy
import logging
import os
import json
from time import time

logger = logging.getLogger()

def create_api():

    consumer_key = ""          # <----
    consumer_secret = ""       # <----  YOU MUST FILL THESE IN
    access_token = ""          # <----  OR THINGS WILL NEVER
    access_token_secret = ""   # <----  WORK.


    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, 
        wait_on_rate_limit_notify=True)
    
    try:
        api.verify_credentials()
        logger.info('doing something')
        with open('api_logging.log', 'w') as f:
            json.dump(str(time()) + " Logged in ok", f)

    except Exception as e:
        print('An error occurredin the config.py file...')
        print(e)
        
        raise e
    logger.info("API created")
    return api