from markov import MarkovChain
from random import choice
from tweepy import API
from tweepy import OAuthHandler
from tweepy import Stream
from tweet_collector import TweetCollector

consumer_key=""
consumer_secret=""
access_token=""
access_token_secret=""

if __name__ == '__main__':
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = API(auth)

    # Get worldwide trending topics on Twiiter
    trends = api.trends_place(1)
    data = trends[0]
    trending = [ trend['name'] for trend in data['trends'] ]
    print("Trending topics")
    for topic in trending:
        print(topic)

    print("Choosing a topic at random...")
    topic = choice(trending)
    print("Chose", topic)

    # Get tweets about the topic
    collector = TweetCollector()
    stream = Stream(auth, collector)
    stream.filter(track = [topic])
    print('Finished collecting tweets')
    tweets = collector.get_tweets()
    for tweet in tweets:
        print(tweet)

