# -*- coding: utf-8 -*-

# @memo_guerra_bot is a Twitter bot publishing the names of victims of the Spanish war and Franco's regime
# We created this bot during a Datathon organized on the topic of the Spanish war and exile organized on January 30 2020 in Poitiers by the eC@NA project.
# This bot uses data as they were published on https://memoriahistorica.org.es/listados-de-victimas/ on January 30 2020.
# This code was written by Alix Chagué. 

import time
import requests # use pip install requests
import tweepy # use pip install tweepy
#from data import EXTRACTED_NAMES


def load_data() -> str or bool:
    """open a csv file, pick up the first line and return its content and update the csv"""
    with open("data.csv", "r") as fh:
        data = fh.read()
    data = data.split("\n")
    data = [] if data == [""] else data
    if len(data) > 1:
        wr = "\n".join(data[1:])
        with open("data.csv", "w") as fh:
            fh.write(wr)
        return data[0]
    elif len(data) == 1:
        with open("data.csv", "w") as fh:
            fh.write("")
        return data[0]
    else:
        print("[NO MORE DATA]")
        return False


def create_message(name:str) -> str:
	"""build a string (the content of the tweet), test its length (no more than 280) and return it"""
	message = "{personne} fut l'une des victimes de la guerre d'Espagne et du franquisme.".format(personne=name)
	#message = "{personne} - test".format(personne=name)
	assert len(message) < 280,"[TOO LONG] ({}): '{}'".format(len(message), message)
	return message


def post_message(message: str) -> None:
    """Post a tweet"""
    from api_secrets import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET

    # Twitter authentication
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    # posting
    try:
	    api.update_status(status = message)
    except tweepy.error.TweepError as e:
    	#raise e
        pass
    finally:
    	return


def main():
    """start a series of steps leading to the publication of a tweet on @memo_guerra_bot account"""
    for i in range(25):
        name = load_data()
        if name:
            message = create_message(name)
            print("[TEST]: {}".format(message)) # for test
            #post_message(message)
            time.sleep(1)
            #time.sleep(3600) # will post a message every hour
        else:
            print("`data.csv` is most likely empty.")


if __name__ == '__main__':
	main()