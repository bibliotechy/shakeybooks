import pickle
from random import choice, randint
import twitter

class MarkyMarkov():

    def __init__(self, text, limit=140):
        self.nonword = "\n"
        self.stopwords = (".","!","?",)
        self.limit = limit
        self.text = text
        try:
            with open("picklespear", "rb") as shake:
                self.table = pickle.load(shake)
                print "loaded the pickle"
        except IOError:
            self.table = {}
            self.setupDB()

    def setupDB(self):
        w1, w2 = self.nonword * 2
        for word in self.text.split():
            if word[-1] in self.stopwords:
                word = word[0:-1]
            self.table.setdefault((w1, w2), []).append(word)
            w1, w2 = w2, word
        self.table.setdefault((w1, w2), []).append(word)
        with open("picklespear", "wb") as shake:
            pickle.dump(self.table,shake)
            print "dumped the pickle"


    def build_string(self, seed = None):
        if not seed:
            print choice(self.table.keys())
            #get the first three words
            seed = choice(list(self.table.keys()))
            w1, w2 = seed
            sentence = ' '.join([w1,w2])
            seed_word = ""
            while len(sentence) < self.limit:
                seed_word = self.table[(w1,w2)][randint(0, len(self.table[w1,w2])-1)]
                if len(sentence) + len(seed_word) > self.limit:
                    return sentence.capitalize()
                else:
                    sentence += " " + (seed_word)
                    w1, w2 = w2, seed_word
        return sentence.capitalize()

if __name__ == "__main__":
    with open("shakeybooks.txt", "rb") as book:
        s = MarkyMarkov(book.read())
        sen= s.build_string()
        CK = ""
        CS = ""
        OT = ""
        OS = ""
        api = twitter.Api(consumer_key=CK, consumer_secret=CS,access_token_key=OT,access_token_secret=OS)
        api.PostUpdate(sen)