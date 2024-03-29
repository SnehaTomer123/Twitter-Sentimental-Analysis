import numpy as np
import joblib
from flask import Flask, render_template, request
import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob


class TwitterClient(object):
    def __init__(self):
        consumer_key = 'S1c4NUGN6dSfk2532SH542NYc'
        consumer_secret = 'FjruVgtskYvyo7SWOhMU8ccGpuTJrnGPr7KvjBHUdC18bKVnVy'
        access_token = '1313519883427082240-BjKdqARxSJhRjP8augJUj8h5kvjDc7'
        access_token_secret = 'SoTwrE0ZT0rmoktL1duMZaQ5aoetuQWheLsJ6LB4LOvWJ'
        try:
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            self.auth.set_access_token(access_token, access_token_secret)
            self.api = tweepy.API(self.auth) 
        except: 
            print("Error: Authentication Failed")

    def get_tweet_sentiment(self, tweet):
        analysis = TextBlob(tweet)
        if analysis.sentiment.polarity > 0:
            return 'Positive'
        elif analysis.sentiment.polarity == 0:
            return 'Neutral'
        else:
            return 'Negative'

    def get_tweets(self, query, count=200):
        tweets = []
        try:
            fetched_tweets = self.api.search_tweets(q=query, count=count)
            for tweet in fetched_tweets:
                parsed_tweet = {}
                parsed_tweet['text'] = tweet.text
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
                if tweet.retweet_count > 0:
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
            return tweets

        except tweepy.TweepyException as e:
            print("Error : " + str(e))


def clean_data(token):
    return [item for item in token if
            not item.startswith('@') and not item.startswith('http') and not item.startswith("RT")]


app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('index.html')


@app.route("/search", methods=["GET", "POST"])
def result():
    if request.method == "POST":
        api = TwitterClient()
        query = str(request.form.get("query"))
        tweets = api.get_tweets(query=query, count=25)
        for tweet in tweets:
            my_list = tweet["text"].split()
            for item in range(len(my_list)):
                new_list = clean_data(my_list)
            tweet["text"] = " ".join(new_list)
        pos_cnt, neg_cnt = 0, 0
        for tweet in tweets:
            if tweet["sentiment"] == "Positive":
                pos_cnt += 1
            elif tweet["sentiment"] == "Negative":
                neg_cnt += 1
        return render_template('index.html', your_list=tweets, pos_cnt=pos_cnt, neg_cnt=neg_cnt, count=len(tweets),
                               query=query)


@app.route("/java", methods=["GET", "POST"])
def java():
    return render_template("mood_java.html")

@app.route("/python", methods = ["GET", "POST"])
def python():
    return render_template("mood_python.html")


if __name__ == "__main__":
    app.run(debug=True)
