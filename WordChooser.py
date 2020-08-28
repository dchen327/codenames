import pandas as pd


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
            words += list(codenames_df[col].dropna())
            words += list(codenames_df[col + 1].dropna())
        for col in range(0, len(duet_df.columns), 3):
            words += list(duet_df[col].dropna())
            words += list(duet_df[col + 1].dropna())

    def getWords(self):
        """ Returns a list of 25 words for a game:
        8 words for team 1, 7 words for team 2, 9 neutral, 1 assasin
        """


if __name__ == "__main__":
    wordChooser = WordChooser('codenames_wordlist.xlsx')
