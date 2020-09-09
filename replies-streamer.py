import tweepy
import json
import csv
import dataset
import pymongo
from textblob import TextBlob
from sqlalchemy.exc import ProgrammingError

class MyStreamListener(tweepy.StreamListener):
    # def __init__(self):
        # self.db = MyMongoDBConnection()

    def on_status(self, status):
        if hasattr(status, 'quoted_status'):
            return

        retweeted = False
        if hasattr(status, 'retweeted_status'):
            retweeted = True

        if status.in_reply_to_status_id is not None:
            # Tweet is a reply
            with open('environment.json', 'r') as myfile:
                env=json.loads(myfile.read())

            auth = tweepy.OAuthHandler(env['consumer_key'], env['consumer_secret'])
            auth.set_access_token(env['access_token'], env['access_token_secret'])

            api = tweepy.API(auth)
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
            except:
                return
        else:
            # Tweet is not a reply
            return
            
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["twitter"]
        mycol = mydb["coronavirus-r"]
        
        try:
            text = status.extended_tweet["full_text"]
        except AttributeError:
            text = status.text

        description = status.user.description
        loc = status.user.location
        coords = status.coordinates
        geo = status.geo
        name = status.user.screen_name
        user_created = status.user.created_at
        followers = status.user.followers_count
        id_str = status.id_str
        created = status.created_at
        retweets = status.retweet_count

        if geo is not None:
            geo = json.dumps(geo)

        if coords is not None:
            coords = json.dumps(coords)

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

    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
    # myStream.filter(track=["wildfire","australia","bushfire","NSWfires","NSWfire","pyrocumulonimbus"])
    myStream.filter(track=["coronavirus"]) 
    # writeToFile(data)

if __name__ == '__main__':
    main()