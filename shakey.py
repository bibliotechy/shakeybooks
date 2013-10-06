from settings import *
import redis
from TwitterAPI import TwitterAPI as tapi

from random import choice, randint

class MarkyMarkov():

    def __init__(self, text=None, limit=None):
        self.nonword = "\n"
        self.stopwords = (".","!","?",":")
        self.limit = limit
        redis_url = "localhost"
        #redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
        self.redis = redis.Redis(redis_url)
        self.text = text

    def setupDB(self):
        w1, w2 = self.nonword * 2
        for word in self.text.decode("utf-8-sig").split():
            self.redis.sadd("{!s}:{!s}".format(w1,w2), word.strip("'\""))
            w1, w2 = w2, word
        self.redis.sadd((w1, w2), self.nonword)


    def build_string(self, seed = None):
        if not self.limit:
            limit = randint(90,140)
        if not seed:
            #get the first three words
            seed = self.redis.randomkey()
            w1, w2 = seed.decode().split(":")
            sentence = ' '.join([w1.capitalize(), w2])
            after_stopword = False
            while len(sentence) < limit:
                seed_word = self.redis.srandmember("{}:{}".format(w1, w2))
                if seed_word:
                    word = seed_word.decode("utf-8")
                    seed_word = seed_word.decode("utf-8")
                    if after_stopword:
                        word = word.capitalize()
                    if word[-1] in self.stopwords:
                        after_stopword = True
                    else:
                        after_stopword = False
                    sentence += " " + word
                if seed_word and w2:
                    w1, w2 = w2, seed_word
                else:
                    return sentence
            return sentence

    def tweet(self, sentence):
        api = tapi(CONSUMER_KEY, CONSUMER_SECRET, AUTH_TOKEN, AUTH_SECRET)
        r = api.request('statuses/update',{"status": sentence })
        if r.status_code != 200:
            raise ValueError("The status was not tweeted")



