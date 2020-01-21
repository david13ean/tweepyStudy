import tweepy
import json
import csv
import dataset
import pymongo
from textblob import TextBlob
from sqlalchemy.exc import ProgrammingError

# class MyMongoDBConnection():
#     myclient = pymongo.MongoClient("mongodb://localhost:27017/")
#     mydb = myclient["twitter"]
#     # mycol = mydb["quoted_tweets"]
#     mycol = mydb["junk"]

class MyStreamListener(tweepy.StreamListener):
    # def __init__(self):
        # self.db = MyMongoDBConnection()

    def on_status(self, status):
        if not hasattr(status, 'quoted_status'):
            return

        retweeted = False
        if hasattr(status, 'retweeted_status'):
            retweeted = True

        # if status.in_reply_to_status_id is not None:
        #     # Tweet is a reply
        #     with open('environment.json', 'r') as myfile:
        #         env=json.loads(myfile.read())

        #     auth = tweepy.OAuthHandler(env['consumer_key'], env['consumer_secret'])
        #     auth.set_access_token(env['access_token'], env['access_token_secret'])

        #     api = tweepy.API(auth)
        #     try:
        #         reply_status = api.get_status(status.in_reply_to_status_id, tweet_mode="extended")
        #         try:
        #             reply_text = reply_status.retweeted_status.full_text
        #             print("replied to was extended tweet")
        #         except AttributeError:
        #             reply_text = reply_status.full_text
        #         reply_description = reply_status.user.description
        #         reply_loc = reply_status.user.location
        #         reply_coords = reply_status.coordinates
        #         reply_geo = reply_status.geo
        #         reply_name = reply_status.user.screen_name
        #         reply_user_created = reply_status.user.created_at
        #         reply_followers = reply_status.user.followers_count
        #         reply_id_str = reply_status.id_str
        #         reply_created = reply_status.created_at
        #         reply_retweets = reply_status.retweet_count
        #     except:
        #         return
        # else:
        #     # Tweet is not a reply
        #     return
            
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["twitter"]
        mycol = mydb["test"]
        
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
        coords = status.coordinates
        geo = status.geo
        name = status.user.screen_name
        user_created = status.user.created_at
        followers = status.user.followers_count
        id_str = status.id_str
        created = status.created_at
        retweets = status.retweet_count
        # bg_color = status.user.profile_background_color
        # blob = TextBlob(text)
        # sent = blob.sentiment

        quoted_description = status.quoted_status.user.description
        quoted_name = status.quoted_status.user.screen_name
        quoted_user_created = status.quoted_status.user.created_at
        quoted_followers = status.quoted_status.user.followers_count
        quoted_id_str = status.quoted_status.id_str
        quoted_created = status.quoted_status.created_at
        quoted_retweets = status.quoted_status.retweet_count

        # more about quoted tweets here: https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/intro-to-tweet-json
        
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
                quoted_description = quoted_description, 
                quoted_text = quoted_text, 
                quoted_name = quoted_name, 
                quoted_user_created = quoted_user_created, 
                quoted_followers = quoted_followers, 
                quoted_id_str = quoted_id_str, 
                quoted_created = quoted_created, 
                quoted_retweets = quoted_retweets
            )

                # reply_text = reply_text,
                # reply_description = reply_description,
                # reply_loc = reply_loc,
                # reply_coords = reply_coords,
                # reply_geo = reply_geo,
                # reply_name = reply_name,
                # reply_user_created = reply_user_created,
                # reply_followers = reply_followers,
                # reply_id_str = reply_id_str,
                # reply_created = reply_created,
                # reply_retweets = reply_retweets,
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

    # -------------------------------------------------------

    # tlists = api.lists_all()
    # data = tlists
    # print(len(data))
    # data = api.get_list(list_id=34179516)
    
    # data = api.list_members(list_id=34179516, cursor=-1)
    # for member in data:
    #     print(member)
    # print(len(data))
    # print(data[0])
    # with open('data.txt', 'w') as outfile:
    #     for t in tlists:
    #         outfile.write('%s\n' % t)
    # Help Methods
    # api.search(q[, geocode][, lang][, locale][, result_type][, count][, until][, since_id][, max_id][, include_entities])
    # Returns a collection of relevant Tweets matching a specified query.

    # Trends Methods
    # Returns the locations that Twitter has trending topic information for. The response is an array of “locations” that encode the location’s WOEID (a Yahoo! Where On Earth ID) and some other human-readable information such as a canonical name and country the location belongs in.
    # data = api.trends_available()
    # print(trends)

    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
    # myStream.filter(track=["wildfire","australia","bushfire","NSWfires","NSWfire","pyrocumulonimbus"])
    myStream.filter(track=["nlwx","stormageddon2020","nlweather","nlblizzard"]) 
    # writeToFile(data)

if __name__ == '__main__':
    main()