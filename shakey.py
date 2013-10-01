
from random import choice, randint

class MarkyMarkov():

    def __init__(self, text, limit=140):
        self.nonword = "\n"
        self.stopwords = (".","!","?",)
        self.limit = limit
        self.table = {}
        self.text = text

    def setupDB(self):
        w1, w2 = self.nonword * 2
        for word in self.text.split():
            if word[-1] in self.stopwords:
                word = word[0:-1]
            self.table.setdefault((w1, w2), []).append(word)
            w1, w2 = w2, word
        self.table.setdefault((w1, w2), []).append(word)


    def build_string(self, seed = None):
        if not seed:
            #get the first three words
            seed = choice(list(self.table.keys()))
            w1, w2 = seed
            sentence = ' '.join([w1,w2])
            while len(sentence) < self.limit:
                seed_word = self.table[(w1,w2)][randint(0, len(self.table[w1,w2])-1)]
                sentence += " " + (seed_word)
                w1, w2 = w2, seed_word
        return sentence.capitalize()

