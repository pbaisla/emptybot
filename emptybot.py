from markov import MarkovChain
from random import shuffle, sample, choice
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

    # Get India trending topics on Twitter
    trends = api.trends_place(23424848)
    data = trends[0]
    trending = [ trend['name'] for trend in data['trends'] ]

    print("Choosing 10 topics at random...")
    shuffle(trending)
    topics = sample(trending, 10)
    for topic in topics:
        print(topic)

    # Get tweets about the topic
    collector = TweetCollector()
    stream = Stream(auth, collector)
    stream.filter(track = topics,languages = ['en'])
    print('Finished collecting tweets')

    # Generate "empty" tweets
    tweets = collector.get_tweets()
    mc_model = MarkovChain(tweets)
    mc_model.generate_model()
    mt_tweets = []
    for i in range(50):
        mt_tweets.append(mc_model.generate_text())

    # Choose one at random and update status
    status = choice(mt_tweets)
    print("Tweeting...", status, sep='\n')
    api.update_status(status)
