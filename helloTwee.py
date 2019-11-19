import tweepy
import json

class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        print(status.text)

    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_error disconnects the stream
            return False

def writeToFile(fileText):
    with open('data.json', 'w') as outfile:
        json.dump(fileText, outfile)

def main():
    with open('environment.json', 'r') as myfile:
        env=json.loads(myfile.read())

    auth = tweepy.OAuthHandler(env['consumer_key'], env['consumer_secret'])
    auth.set_access_token(env['access_token'], env['access_token_secret'])

    api = tweepy.API(auth)

    # -------------------------------------------------------

    # Help Methods
    # api.search(q[, geocode][, lang][, locale][, result_type][, count][, until][, since_id][, max_id][, include_entities])
    # Returns a collection of relevant Tweets matching a specified query.

    # Trends Methods
    # Returns the locations that Twitter has trending topic information for. The response is an array of “locations” that encode the location’s WOEID (a Yahoo! Where On Earth ID) and some other human-readable information such as a canonical name and country the location belongs in.
    trends = api.trends_available()
    # print(trends)

    # myStreamListener = MyStreamListener()
    # myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
    # myStream.filter(track=["15675138"])

    writeToFile(trends)

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
