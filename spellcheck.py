import operator
import pandas as pd
import os
from collections import OrderedDict
from nltk.util import ngrams
import collections
from configparser import ConfigParser

cfg = ConfigParser()
cfg.read('./config.ini')


class Correct(object):

    def __init__(self, ngram_size=2, len_variance=1):
        self.ngram_size = ngram_size
        self.len_variance = len_variance

        self.words = set ([w.lower () for w in open (dictionary).read ().split ()])

        # create dictionary of ngrams and the words that contain them
        self.ngram_words = collections.defaultdict (set)

        for word in self.words:
            for ngram in self.ngrams (word):
                self.ngram_words[word].add (ngram)
        print ("Generated %d ngrams from %d words" % (len (self.ngram_words), len (self.words)))

    def ngrams(self, ngram):
        bigram = set ()

        bigram = ngrams (ngram, 2, pad_right=True, pad_left=True, right_pad_symbol=" ", left_pad_symbol=" ")

        return bigram

    def lookup(self, word):
        "Return True if the word exists in the dictionary."
        return word in self.words

    def suggested_words(self, target_word):
        "Given a word, return a list of possible corrections."
        input_dictionary = collections.defaultdict (set)
        for ngram in self.ngrams (target_word):
            input_dictionary[target_word].add(ngram)

        d = set()
        for key, value in input_dictionary.items():
            key1 = key
            c = value

        output = {}
        for key, value in sorted (self.ngram_words.items()):

            if len (key) == len (key1) or len (key) == (len (key1) + 1) or len (key) == (len (key1) - 1):
                d = value.intersection(c)
                if len (d) >= 2:
                    "calculating similarity score"
                    similarity = 2 * len (d) / (len (key) + len (key1))

                    if similarity >=0.70:
                        "checking similarity score"
                         # print (key1, key,":", similarity)
                        
                        output.update({key: similarity})

        sorted_op = OrderedDict(sorted(output.items (), key=operator.itemgetter(1), reverse=True))
        
        items = list (sorted_op.items ())
        if not items:
            pass

        else:
            corrected_dict = {"input_word": key1, "output_word": items[0][0]}
            corrected_file = pd.DataFrame.from_dict (corrected_dict, orient='index').transpose ()
            if not os.path.isfile (cfg.get('pathParams', 'check_output')):
                corrected_file.to_csv (cfg.get('pathParams', 'check_output'), header="column_names", index=False)
            else:
                corrected_file.to_csv(cfg.get('pathParams', 'check_output'), mode="a",header=False, index=False)


dictionary = cfg.get('pathParams', 'dictionary_path')

if __name__ == '__main__':

    autocorrect = Correct ()

path = cfg.get('pathParams', 'error_wordlist')
print("Generating output")
with open (path) as f:
    word_split=f.read().strip().split()


for words in word_split:

    word = words.lower ()

    if len(word)<=3 or autocorrect.lookup (word):
        pass

    else:
        sugg = autocorrect.suggested_words (word)
print("output generated")