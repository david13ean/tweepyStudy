import tweepy
import json
import csv
import sys
import dataset
import pymongo
from textblob import TextBlob
from sqlalchemy.exc import ProgrammingError

class MyStreamListener(tweepy.StreamListener):
    def __init__(self, db, col):
        self.db = db
        self.col = col
        print(col)

    def on_status(self, status, db, col):
        with open('environment.json', 'r') as myfile:
            env=json.loads(myfile.read())

        auth = tweepy.OAuthHandler(env['consumer_key'], env['consumer_secret'])
        auth.set_access_token(env['access_token'], env['access_token_secret'])

        api = tweepy.API(auth)
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient[db]
        mycol = mydb[col+"g"]

        geo = ""
        coords = ""
        retweeted = False
        if hasattr(status, 'retweeted_status'):
            retweeted = True

        if status.geo is not None:
            geo = json.dumps(geo)

        if status.coordinates is not None:
            coords = json.dumps(coords)

        if hasattr(status, 'quoted_status'):
            mycol = mydb[col+"q"]
            
            try:
                text = status.extended_tweet["full_text"]
            except AttributeError:
                text = status.text
            
            try:
                quoted_text = status.quoted_status.extended_tweet["full_text"]
            except AttributeError:
                quoted_text = status.quoted_status.text

            description = status.user.description
            loc = status.user.location
            name = status.user.screen_name
            user_created = status.user.created_at
            followers = status.user.followers_count
            id_str = status.id_str
            created = status.created_at
            retweets = status.retweet_count
            quoted_description = status.quoted_status.user.description
            quoted_name = status.quoted_status.user.screen_name
            quoted_user_created = status.quoted_status.user.created_at
            quoted_followers = status.quoted_status.user.followers_count
            quoted_id_str = status.quoted_status.id_str
            quoted_created = status.quoted_status.created_at
            quoted_retweets = status.quoted_status.retweet_count

            mycol.insert_one(
                dict(
                    description = description, 
                    loc = loc, 
                    text = text, 
                    coords = coords, 
                    geo = geo, 
                    name = name, 
                    user_created = user_created, 
                    followers = followers, 
                    id_str = id_str, 
                    created = created, 
                    retweets = retweets,
                    retweeted = retweeted,
                    quoted_description = quoted_description, 
                    quoted_text = quoted_text, 
                    quoted_name = quoted_name, 
                    quoted_user_created = quoted_user_created, 
                    quoted_followers = quoted_followers, 
                    quoted_id_str = quoted_id_str, 
                    quoted_created = quoted_created, 
                    quoted_retweets = quoted_retweets
                )
            )
            return

        try:
            text = status.extended_tweet["full_text"]
        except AttributeError:
            text = status.text

        if status.in_reply_to_status_id is not None:
            # Tweet is a reply
            mycol = mydb[col+"r"]
            try:
                reply_status = api.get_status(status.in_reply_to_status_id, tweet_mode="extended")
                try:
                    reply_text = reply_status.retweeted_status.full_text
                    print("replied to was extended tweet")
                except AttributeError:
                    reply_text = reply_status.full_text
                reply_description = reply_status.user.description

                reply_loc = reply_status.user.location
                reply_coords = reply_status.coordinates
                reply_geo = reply_status.geo
                reply_name = reply_status.user.screen_name
                reply_user_created = reply_status.user.created_at
                reply_followers = reply_status.user.followers_count
                reply_id_str = reply_status.id_str
                reply_created = reply_status.created_at
                reply_retweets = reply_status.retweet_count

                mycol.insert_one(
                    dict(
                        description = status.user.description,
                        loc = status.user.location,
                        text = text, 
                        coords = status.coordinates,
                        geo = status.geo,
                        name = status.user.screen_name,
                        user_created = status.user.created_at,
                        followers = status.user.followers_count,
                        id_str = status.id_str,
                        created = status.created_at,
                        retweets = status.retweet_count,
                        
                        retweeted = retweeted,
                        reply_text = reply_text,
                        reply_description = reply_description,
                        reply_loc = reply_loc,
                        reply_coords = reply_coords,
                        reply_geo = reply_geo,
                        reply_name = reply_name,
                        reply_user_created = reply_user_created,
                        reply_followers = reply_followers,
                        reply_id_str = reply_id_str,
                        reply_created = reply_created,
                        reply_retweets = reply_retweets,
                    )

                )
                return
            except:
                return
        else:
            mycol.insert_one(
                dict(
                    description = status.user.description,
                    loc = status.user.location,
                    text = text, 
                    coords = status.coordinates,
                    geo = status.geo,
                    name = status.user.screen_name,
                    user_created = status.user.created_at,
                    followers = status.user.followers_count,
                    id_str = status.id_str,
                    created = status.created_at,
                    retweets = status.retweet_count,
                    retweeted = retweeted
                )

            )
        

    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_error disconnects the stream
            return False

def writeToFile(fileText):
    with open('data.json', 'w') as outfile:
        # outfile.truncate(0)
        json.dump(fileText, outfile)

def main():
    with open('environment.json', 'r') as myfile:
        env=json.loads(myfile.read())

    auth = tweepy.OAuthHandler(env['consumer_key'], env['consumer_secret'])
    auth.set_access_token(env['access_token'], env['access_token_secret'])

    api = tweepy.API(auth)
    myStreamListener = MyStreamListener(sys.argv[1],sys.argv[2])
    myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
    # myStream.filter(track=["wildfire","australia","bushfire","NSWfires","NSWfire","pyrocumulonimbus"])
    myStream.filter(track=["coronavirus","COVID-19"]) 
    # writeToFile(data)

if __name__ == '__main__':
    main()