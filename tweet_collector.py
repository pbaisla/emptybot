from tweepy.streaming import StreamListener

class TweetCollector(StreamListener):
    def __init__(self, limit = 100, api = None):
        super(TweetCollector, self).__init__()
        self.limit = limit
        self.count = 0
        self.tweets = []

    def on_status(self, tweet):
        self.tweets.append(tweet.text)
        self.count += 1
        if self.count % 10 == 0:
            print("Collected", self.count, "tweets")
        if self.count == self.limit:
            return False

    def on_error(self, status):
        print(status, "An error occured.")

    def get_tweets(self):
        return self.tweets
