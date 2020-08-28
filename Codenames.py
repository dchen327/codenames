"""
The class Codenames.py either takes in a list of user provided words, or 
generates words through the WordChooser class. It then attempts to play as the
spymaster, giving clues for each team.

Author: David Chen
"""
from gensim.test.utils import datapath, get_tmpfile
from gensim.models import KeyedVectors
from gensim.scripts.glove2word2vec import glove2word2vec


class Codenames:
    def __init__(self):
        """ Load in Stanford GloVe vectors and initialize model """
        # glove_file = '/home/dchen327/Downloads/GloVe/glove.6B.300d.txt'
        # word2vec_glove_file = get_tmpfile('glove.6B.300d.word2vec.txt')
        # glove2word2vec(glove_file, word2vec_glove_file)
        # model = KeyedVectors.load_word2vec_format(word2vec_glove_file)
        # model.save('glove_model.bin')

        self.model = KeyedVectors.load('glove_model.bin')


if __name__ == "__main__":
    codenames = Codenames()
    print(codenames.model.most_similar('banana'))
