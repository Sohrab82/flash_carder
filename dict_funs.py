from datetime import datetime, timedelta
import pandas as pd
import csv
import os
import glob


class Word:
    def __init__(self):
        self.word = None
        self.translation = None
        self.passed = 0
        self.failed = 0
        self.last_date = datetime.today() - timedelta(days=1)

    def onFail(self):
        self.failed += 1
        self.last_date = datetime.today()

    def onPass(self):
        self.passed += 1
        self.last_date = datetime.today()

    def onKeep(self):
        # do nothing, i just saw the word again
        pass

    def should_show(self, cur_date):
        if self.last_date == None:
            self.last_date = cur_date
            return True
        if (cur_date - self.last_date).days < 1:
            # I asked today, not again
            return False
        if self.passed - self.failed < 3:
            # still not confident enough
            return True
        else:
            # confident
            if (cur_date - self.last_date).days > 15:
                # last time was asked 15 days ago
                return True
            else:
                return False


class DictHandler:
    def __init__(self):
        self.dictionary = []

    def load_google_dict(self, google_csv):
        df = pd.read_excel(google_csv, header=None)
        words = df.values[:, 2]
        translations = df.values[:, 3]
        lang1 = df.values[:, 0]
        lang2 = df.values[:, 0]
        lang1 = [word.strip().lower() for word in lang1]
        lang2 = [word.strip().lower() for word in lang2]
        words = [word.strip().lower() for word in words]
        translations = [word.strip().lower() for word in translations]
        for i in range(len(words)):
            # if lang1[i] != 'swedish' and lang2[i] != 'swedish':
            #     continue
            found = False
            for j in range(len(self.dictionary)):
                if self.dictionary[j].word == words[i]:
                    # word already defined
                    if self.dictionary[j].translation == translations[i]:
                        # translation are the same
                        found = True
                        break
                    else:
                        # if translation is not already in the dictionary
                        if self.dictionary[j].translation.find(translations[i]) == -1:
                            self.dictionary[j].translation = self.dictionary[j].translation + \
                                ', ' + translations[i]
                        found = True
                        break
            if found:
                continue
            w = Word()
            w.word = words[i]
            w.translation = translations[i]
            self.dictionary.append(w)

            w = Word()
            w.word = translations[i]
            w.translation = words[i]
            self.dictionary.append(w)

    def load_dict(self):
        # load default dictionary
        if os.path.exists('db.csv'):
            df = pd.read_csv("db.csv", header=None, delimiter='_')
            words = df.values[:, 0]
            translations = df.values[:, 1]
            passed = df.values[:, 2]
            failed = df.values[:, 3]
            last_date = df.values[:, 4]

            words = [word.strip().lower() for word in words]
            translations = [word.strip().lower() for word in translations]
            for i in range(len(words)):
                w = Word()
                w.word = words[i]
                w.translation = translations[i]
                w.passed = int(passed[i])
                w.failed = int(failed[i])
                w.last_date = datetime.strptime(last_date[i], '%Y-%m-%d')
                self.dictionary.append(w)
        # load all xlsx files in this folder and add them to my db
        for file in glob.glob('google_files/*.xlsx'):
            print('Loading ', file)
            self.load_google_dict(file)

    def save_dict(self):
        print('Saving dictionary..')
        with open('db.csv', mode='w', encoding="utf-8") as db_file:
            db_writer = csv.writer(
                db_file, delimiter='_', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for item in self.dictionary:
                db_writer.writerow(
                    [item.word, item.translation, item.passed, item.failed, item.last_date.strftime('%Y-%m-%d')])

    def export_as_word(self):
        print('Exporting dictionary as list.csv..')
        with open('list.csv', mode='w', encoding="utf-8") as db_file:
            db_writer = csv.writer(
                db_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            # skip en-sw translations
            skip = False
            for item in self.dictionary:
                if skip:
                    skip = False
                    continue
                db_writer.writerow(
                    [item.word, item.translation])
                skip = True
