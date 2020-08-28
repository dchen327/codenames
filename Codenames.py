"""
The class Codenames.py either takes in a list of user provided words, or 
generates words through the WordChooser class. It then attempts to play as the
spymaster, giving clues for each team.

Author: David Chen
"""
import pathlib
import itertools
import time
from gensim.test.utils import datapath, get_tmpfile
from gensim.models import KeyedVectors
from gensim.scripts.glove2word2vec import glove2word2vec
from WordChooser import WordChooser


class Codenames:
    def __init__(self, word_roles=None):
        self.load_glove()
        if word_roles is None:  # generate from WordChooser
            wordChooser = WordChooser('codenames_wordlist.xlsx')
            self.word_roles = wordChooser.getWords()
        else:
            self.word_roles = word_roles

    def load_glove(self):
        """ Load in Stanford GloVe vectors and initialize model """
        model_file = pathlib.Path('glove_model.bin')
        print('Gathering GloVe vectors...')
        if model_file.exists():
            self.model = KeyedVectors.load('glove_model.bin')
        else:
            print('Loading glove file from disk')
            glove_file = '/home/dchen327/Downloads/GloVe/glove.6B.300d.txt'
            word2vec_glove_file = get_tmpfile('glove.6B.300d.word2vec.txt')
            glove2word2vec(glove_file, word2vec_glove_file)
            self.model = KeyedVectors.load_word2vec_format(word2vec_glove_file)
            self.model.save('glove_model.bin')

    def get_clues(self):
        """ Get clues for both players """
        score_threshold = 0.3
        for team_num in range(1, 3):
            scores_by_len = {}
            team_words = self.word_roles[f'Team {team_num}']
            oppo_words = self.word_roles[f'Team {3 - team_num}']
            for group_size in range(4, 2, -1):  # start with larger word groups
                scores = {}
                assassin_word = self.word_roles['Assassin']
                for word_group in itertools.combinations(team_words, group_size):
                    result = self.model.most_similar_cosmul(
                        positive=list(word_group), negative=[assassin_word], topn=1)
                    if result[0][1] > score_threshold:
                        scores[word_group] = result[0]
                # sort in descending order by scores
                scores = {k: v for k, v in sorted(
                    scores.items(), key=lambda x: x[1][1], reverse=True)}
                scores_by_len[group_size] = scores
            print(f'TEAM {team_num}: ')
            used_clues = set()
            for scores in scores_by_len.values():
                for i, (word_group, (clue, score)) in enumerate(scores.items()):
                    if clue not in used_clues:
                        used_clues.add(clue)
                        print(clue, word_group, f'{score:.3f}')


if __name__ == "__main__":
    word_roles = {
        'Team 1': ['boom', 'tooth', 'chest', 'santa', 'copper', 'cane', 'conductor', 'jeweler'],
        'Team 2': ['nut', 'elephant', 'honey', 'crystal', 'paper', 'sling', 'window'],
        'Neutral': ['drum', 'spot', 'jet', 'engine', 'dream', 'crane', 'slug', 'track', 'desk'],
        'Assassin': 'lawyer'
    }
    # codenames = Codenames(word_roles=word_roles)
    start_time = time.time()
    codenames = Codenames(word_roles=None)
    print(codenames.get_clues())
    print(f'Finished in {time.time() - start_time:.3f}')
