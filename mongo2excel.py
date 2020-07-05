import pandas as pd
import sys
from pymongo import MongoClient

def delete_unneeded_cols(df):
    del df['_id']
    del df['coords']
    del df['geo']

    # del df['loc']
    # del df['description']
    # del df['followers']
    # del df['quoted_followers']
    # del df['retweets']
    # del df['quoted_id_str']
    # del df['quoted_description']
    # del df['quoted_retweets']
    # del df['retweeted']
    # del df['id_str']
    # del df['user_created']
    # del df['quoted_user_created']

    # del df['text']
    # del df['quoted_text']

    # del df['name']
    # del df['quoted_name']
    # del df['created']
    # del df['quoted_created']
    return df

def _connect_mongo(host, port, username, password, db):
    """ A util for making a connection to mongo """

    if username and password:
        mongo_uri = 'mongodb://%s:%s@%s:%s/%s' % (username, password, host, port, db)
        conn = MongoClient(mongo_uri)
    else:
        conn = MongoClient(host, port)
    return conn[db]


def read_mongo(count, limit, query={}, host='localhost', port=27017, username=None, password=None, no_id=True):
    """ Read from Mongo and Store into DataFrame """

    # Connect to MongoDB
    db = _connect_mongo(host=host, port=port, username=username, password=password, db="twitter")

    dfMain = pd.DataFrame()
    dbList = ["coronavirus", "cvq2", "cv3-q", "cv4-q", "cv5-q"]
    for collection in dbList:
        cursor = db[collection].find().limit(limit)

        # Expand the cursor and construct the DataFrame
        df = pd.DataFrame(list(cursor))

        # stack the DataFrames on top of each other
        dfMain = pd.concat([dfMain, df.sample(count)])
        dfMain = dfMain.reset_index(drop=True)
          
    return dfMain

def col_formatter(df):
    # This removes retweet evidence, twitter links, and whitespace in preparation for duplicate removal
    df['text'] = df['text'].str.replace('\n', ' ', regex=True).replace('\r', '', regex=True).replace().replace('\t', ' ', regex=True).replace(r'(RT @\w*:\s)', '', regex=True).replace(r'(\shttps?:\/\/t\.co\/\w*)', '', regex=True)
    df['quoted_text'] = df['quoted_text'].str.replace('\n', ' ', regex=True).replace('\r', '', regex=True).replace().replace('\t', ' ', regex=True).replace(r'(RT @\w*:\s)', '', regex=True).replace(r'(https?:\/\/t\.co\/\w*)', '', regex=True)
    # removes multi whitespace
    df['text'] = df['text'].str.strip()
    df['quoted_text'] = df['quoted_text'].str.strip()
    df = df.drop_duplicates(subset=['text', 'quoted_text'])
    return df

if __name__ == '__main__':
    count = int(sys.argv[1]) 
    limit = int(sys.argv[3])            
    print(sys.argv)
    df = read_mongo(count, limit)
    df = delete_unneeded_cols(df)
    df = col_formatter(df)

    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        print("the last things to be printed:\n\nLIST")
        print(df['text'])
        print(df['quoted_text'])
    df.to_excel(sys.argv[2])