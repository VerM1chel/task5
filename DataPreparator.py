import re
import string

import pandas as pd


class DataPreparator:
    def __init__(self, path):
        self.data = pd.read_csv(path)

    def prepare_data(self):
        # Delete all rows where all values are NaN
        for i in range(self.data.shape[0]):
            if all(self.data.loc[i].isna()):
                self.data.drop(i, axis=0, inplace=True)
        self.data.fillna("-", inplace=True)
        self.data.sort_values(by="at", inplace=True)

    def clean_text(self):
        for i in range(0, len(self.data)):
            # Remove special symbols
            self.data.replyContent[i] = re.sub('\n', ' ', str(self.data['replyContent'][i]))
            # Remove all symbols except letters
            self.data.replyContent[i] = re.sub(f'[^a-zA-Z{string.punctuation}]', ' ', str(self.data['replyContent'][i]))
            # Replacing all gaps with spaces
            self.data.replyContent[i] = re.sub(r'\s+', ' ', self.data.replyContent[i])
            self.data['score'].astype(int)
            self.data['thumbsUpCount'].astype(int)

    def save_to_csv(self, path_to_save):
        self.data.to_csv(path_to_save, index=False)
