import tweepy
import json
import csv
import sys
import dataset
import pymongo
from textblob import TextBlob
from sqlalchemy.exc import ProgrammingError

class MyStreamListener(tweepy.StreamListener):
    db = "twitter"
    col = "test"

    def getRetweeted(self, status):
        if hasattr(status, 'retweeted_status'): return True
        else: return False
    
    def getGeo(self, status):
        if status.geo is not None:
            return json.dumps(status.geo)
        else: return ""

    def getCoords(self, status):
        if status.coordinates is not None:
            return json.dumps(status.coordinates)
        else: return ""
    
    def getText(self, status):
        try:
            text = status.extended_tweet["full_text"]
        except AttributeError:
            text = status.text
        return text

    def getQuoteText(self, status):
        try:
            quoted_text = status.quoted_status.extended_tweet["full_text"]
        except AttributeError:
            quoted_text = status.quoted_status.text
        return quoted_text

    def logQuoteTweet(self, status):
        self.col = self.col+"q"
        text = getText(status)
        quoted_text = getQuoteText(status)

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

        return dict(
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
    
    def logReplyTweet(self, status):
        self.col = self.col+"r"
        try:
            reply_status = api.get_status(status.in_reply_to_status_id, tweet_mode="extended")
            try:
                reply_text = reply_status.retweeted_status.full_text
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

            return dict(
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
        except:
            return

    def on_status(self, status):
        with open('environment.json', 'r') as myfile:
            env=json.loads(myfile.read())

        auth = tweepy.OAuthHandler(env['consumer_key'], env['consumer_secret'])
        auth.set_access_token(env['access_token'], env['access_token_secret'])

        api = tweepy.API(auth)
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient[self.db]
        mycol = mydb[self.col+"g"]

        self.geo = getGeo(status)
        self.coords = getCoords(status)
        self.retweeted = getRetweeted(status)

        if hasattr(status, 'quoted_status'):
            # Tweet is a quote
            logQuoteTweet(status)

        if status.in_reply_to_status_id is not None:
            # Tweet is a reply
            logReplyTweet(status)

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
    myStreamListener = MyStreamListener()
    myStreamListener.db = sys.argv[1]
    myStreamListener.col = sys.argv[2]
    myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
    # myStream.filter(track=["wildfire","australia","bushfire","NSWfires","NSWfire","pyrocumulonimbus"])
    myStream.filter(track=["coronavirus","COVID-19"]) 
    # writeToFile(data)

if __name__ == '__main__':
    main()