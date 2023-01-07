from User import *


class Tweet:
    default_tweet_id = 0

    def __init__(self, massage, user: User, parent_id=None):
        self.likes_of_tweet = []
        self.retweets_of_tweet = []
        self.comments = []
        self.massage = massage
        self.time_of_tweet = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        self.author = user
        self.parent_id = parent_id

        Tweet.default_tweet_id += 1
        self.tweet_id = Tweet.default_tweet_id

    def __repr__(self):
        return f'== tweet ins == "{self.massage}"|'

    def __str__(self):
        return f'{self.massage}'



