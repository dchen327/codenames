import pandas as pd
import random


class WordChooser:
    def __init__(self, spreadsheet_name):
        self.words = []
        self.readFromXlsx(spreadsheet_name)

    def readFromXlsx(self, spreadsheet_name):
        """ Read a list of words stored in spreadsheet """
        sheets = pd.read_excel(spreadsheet_name, sheet_name=None, header=None)
        codenames_df = sheets['Codenames']
        duet_df = sheets['Duet']

        # format of spreadsheet: 2 columns, then a column of Nan
        for col in range(0, len(codenames_df.columns), 3):
            self.words += list(codenames_df[col].dropna())
            self.words += list(codenames_df[col + 1].dropna())
        for col in range(0, len(duet_df.columns), 3):
            self.words += list(duet_df[col].dropna())
            self.words += list(duet_df[col + 1].dropna())

    def getWords(self):
        """ Returns a list of 25 words for a game:
        8 words for team 1, 7 words for team 2, 9 neutral, 1 assassin
        """
        curr_words = random.sample(self.words, 25)
        word_roles = {
            'Team 1': curr_words[:8],
            'Team 2': curr_words[8: 15],
            'Neutral': curr_words[15: 24],
            'Assassin': curr_words[24],
        }
        return word_roles


if __name__ == "__main__":
    wordChooser = WordChooser('codenames_wordlist.xlsx')
    words_roles = wordChooser.getWords()
    print(words_roles)
