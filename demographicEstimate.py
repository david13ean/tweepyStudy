import sys
import datetime
import pandas as pd
from pymongo import MongoClient
from langdetect import detect
import mongo2excel

def guessLanguage(phrase):
    try:
        return detect(phrase)
    except:
        return "na"

def read_mongo(limit, query={}, host='localhost', port=27017, username=None, password=None, no_id=True):
    """ Read from Mongo and Store into DataFrame """

    # Connect to MongoDB
    db = mongo2excel._connect_mongo(host=host, port=port, username=username, password=password, db="twitter")

    dbList = ["coronavirus", "cvq2", "cv3-q", "cv4-q", "cv5-q"]
    for collection in dbList:
        cursor = db[collection].find().limit(limit)
        df = pd.DataFrame(list(cursor))
        generateColReport(df, collection)

def generateColReport(df, collection):
    print("\nCategorizing " + collection + " from dbList")
    # Expand the cursor and construct the DataFrame
    df['text_lang'] = df['text'].apply(guessLanguage)
    df['quoted_text_lang'] = df['quoted_text'].apply(guessLanguage)
    print("Language statistics:")
    print(df['text_lang'].value_counts())

    print("Set time range:")
    print(df['created'].iat[0].strftime('%m/%d/%Y, %H:%M:%S') + " through " + df['created'].iat[-1].strftime('%m/%d/%Y, %H:%M:%S'))

if __name__ == '__main__':
    limit = int(sys.argv[1])
    read_mongo(limit)