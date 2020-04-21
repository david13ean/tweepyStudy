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
import imperativeMarker


def main():
    myClient = pymongo.MongoClient("mongodb://localhost:27017/")
    myDb = myClient[sys.argv[1]]
    mycol = myDb[sys.argv[2]]

    print ("\nReturn every document:")
    count = 10

    tt = TweetTokenizer()
    df = pd.DataFrame(list(mycol.find()))
    df['tokenized_tweet'] = df['text'].apply(tt.tokenize)
    df['quoted_tokenized_tweet'] = df['quoted_text'].apply(tt.tokenize)

    df['tweet_pos'] = df['tokenized_tweet'].apply(nltk.pos_tag)
    df['quoted_tweet_pos'] = df['quoted_tokenized_tweet'].apply(nltk.pos_tag)

    sid = SentimentIntensityAnalyzer()
    df['tweet_polarity'] = df['text'].apply(sid.polarity_scores)
    df['quoted_tweet_polarity'] = df['quoted_text'].apply(sid.polarity_scores)
    
    df['tweet_imperative'] = df['tweet_pos'].apply(sid.polarity_scores)
    df['quoted_tweet_imperative'] = df['quoted_tweet_pos'].apply(sid.polarity_scores)


    print(df.loc[0])
    # newcol = myDb["sentiment"]
    # records = json.loads(df.T.to_json()).values()
    # myDb.newcol.insert_many(df.to_dict('records'))
    

if __name__ == '__main__':
    main()