import pymongo
import numpy as np 
import pandas as pd 
import json
import re
import sys
import matplotlib.pyplot as plt
import nltk
from nltk.tokenize import TweetTokenizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from imperativeMarker import is_imperative


def main():
    myClient = pymongo.MongoClient("mongodb://localhost:27017/")
    myDb = myClient[sys.argv[1]]
    mycol = myDb[sys.argv[2]]
    count = int(sys.argv[3])

    tt = TweetTokenizer()
    df = pd.DataFrame(list(mycol.find().limit(count)))

    # collection broken up into words
    df['tokenized_tweet'] = df['text'].apply(tt.tokenize)
    df['quoted_tokenized_tweet'] = df['quoted_text'].apply(tt.tokenize)

    # words labeled with part of speech tag 
    df['tweet_pos'] = df['tokenized_tweet'].apply(nltk.pos_tag)
    df['quoted_tweet_pos'] = df['quoted_tokenized_tweet'].apply(nltk.pos_tag)

    # polarity measured from collective word scores
    sid = SentimentIntensityAnalyzer()
    df['tweet_polarity'] = df['text'].apply(sid.polarity_scores)
    df['quoted_tweet_polarity'] = df['quoted_text'].apply(sid.polarity_scores)
    
    # imperative mood measured from imperative marker function 
    df['tweet_imperative'] = df['tweet_pos'].apply(is_imperative)
    df['quoted_tweet_imperative'] = df['quoted_tweet_pos'].apply(is_imperative)

    # print everything that is imperative into excel file
    df.loc[(df['quoted_tweet_imperative'] == True) | (df['tweet_imperative'] == True)].to_csv('output.csv')

    # pd.set_option("display.max_rows", None, "display.max_columns", None)
    # print(df.loc[df['tweet_imperative'] == True].to_string())
    # newcol = myDb["sentiment"]
    # records = json.loads(df.T.to_json()).values()
    # myDb.newcol.insert_many(df.to_dict('records'))

if __name__ == '__main__':
    main()