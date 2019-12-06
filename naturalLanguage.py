import pymongo
import numpy as np 
import pandas as pd 
import re
import matplotlib.pyplot as plt
from nltk.tokenize import TweetTokenizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["twitter"]
mycol = mydb["junk"]

print ("\nReturn every document:")
count = 1

tt = TweetTokenizer()
df = pd.DataFrame(list(mycol.find()))
df['tokenized_tweet'] = df['text'].apply(tt.tokenize)
df['quoted_tokenized_tweet'] = df['quoted_text'].apply(tt.tokenize)

sid = SentimentIntensityAnalyzer()
df['tweet_polarity'] = df['text'].apply(sid.polarity_scores)

print(df.loc[0])
# for col in df.columns:
#     print(df[col])
#     count = count - 1
#     print(count)
#     # if count <= 0:
#     #     break

# for doc in mycol.find():
#     print (doc)
#     count = count - 1
#     if count <= 0:
#         break
