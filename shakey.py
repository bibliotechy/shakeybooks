import os
import redis
from random import choice, randint

class MarkyMarkov():

    def __init__(self, text, limit=140):
        self.nonword = "\n"
        self.stopwords = (".","!","?",)
        self.limit = limit
        redis_url = "localhost"
        #redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
        self.redis = redis.Redis(redis_url)
        self.text = text

    def setupDB(self):
        w1, w2 = self.nonword * 2
        for word in self.text.split():
            if word[-1] in self.stopwords:
                word = word[0:-1]
            self.redis.sadd((w1, w2), word)
            w1, w2 = w2, word
        self.redis.sadd((w1, w2), self.nonword)


    def build_string(self, seed = None):
        if not seed:
            #get the first three words
            seed = self.redis.randomkey()
            w1, w2 = seed.translate(None, "()',").split()
            sentence = ' '.join([w1, w2])
            while len(sentence) < self.limit:
                seed_word = self.redis.srandmember("('%s', '%s')".format(w1, w2))
                sentence += " " + (seed_word)
                w1, w2 = w2, seed_word
        return sentence.capitalize()

