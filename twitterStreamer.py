import tweepy
import json

class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        if status.retweeted:
            return

        description = status.user.description
        loc = status.user.location
        text = status.text
        coords = status.coordinates
        geo = status.geo
        name = status.user.screen_name
        user_created = status.user.created_at
        followers = status.user.followers_count
        id_str = status.id_str
        created = status.created_at
        retweets = status.retweet_count
        bg_color = status.user.profile_background_color
        blob = TextBlob(text)
        sent = blob.sentiment
        print (text)

        if geo is not None:
            geo = json.dumps(geo)

        if coords is not None:
            coords = json.dumps(coords)  
                                           
        table = db[settings.TABLE_NAME]
        try:
            table.insert(dict(
               user_description=description,
               user_location=loc,
               coordinates=coords,
               text=text,
               geo=geo,
               user_name=name,
               user_created=user_created,
               user_followers=followers,
               id_str=id_str,
               created=created,
               retweet_count=retweets,
               user_bg_color=bg_color,
               polarity=sent.polarity,
               subjectivity=sent.subjectivity,
            ))
    
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

    tlists = api.lists_all()
    data = tlists
    print(len(data))
    # data = api.get_list(list_id=34179516)
    
    data = api.list_members(list_id=34179516, cursor=-1)
    # for member in data:
    #     print(member)
    print(len(data))
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

    # myStreamListener = MyStreamListener()
    # myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
    # myStream.filter(track=["programming"])

    # writeToFile(data)

if __name__ == '__main__':
    main()

    # public_tweets = api.home_timeline()
    # for tweet in public_tweets:
    #     print(tweet.text)

    # https://tweepy.readthedocs.io/en/latest/api.html#api-reference

    # api.statuses_lookup(id_[, include_entities][, trim_user][, map_][, include_ext_alt_text][, include_card_uri])
    # Returns full Tweet objects for up to 100 tweets per request, specified by the id_ parameter.

    # api.user_timeline([id/user_id/screen_name][, since_id][, max_id][, count][, page])
    # Returns the 20 most recent statuses posted from the authenticating user or the user specified. It’s also possible to request another user’s timeline via the id parameter.

    # api.retweets_of_me([since_id][, max_id][, count][, page])
    # Returns the 20 most recent tweets of the authenticated user that have been retweeted by others.

    # api.mentions_timeline([since_id][, max_id][, count])
    # Returns the 20 most recent mentions, including retweets.

    # api.get_status(id[, trim_user][, include_my_retweet][, include_entities][, include_ext_alt_text][, include_card_uri])
    # Returns a single status specified by the ID parameter.
