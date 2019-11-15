import tweepy
import json

with open('environment.json', 'r') as myfile:
    env=json.loads(myfile.read())

auth = tweepy.OAuthHandler(env['consumer_key'], env['consumer_secret'])
auth.set_access_token(env['access_token'], env['access_token_secret'])

api = tweepy.API(auth)

# public_tweets = api.home_timeline()
# for tweet in public_tweets:
#     print(tweet.text)

# https://tweepy.readthedocs.io/en/latest/api.html#api-reference

# API.statuses_lookup(id_[, include_entities][, trim_user][, map_][, include_ext_alt_text][, include_card_uri])
# Returns full Tweet objects for up to 100 tweets per request, specified by the id_ parameter.

# API.user_timeline([id/user_id/screen_name][, since_id][, max_id][, count][, page])
# Returns the 20 most recent statuses posted from the authenticating user or the user specified. It’s also possible to request another user’s timeline via the id parameter.

# API.retweets_of_me([since_id][, max_id][, count][, page])
# Returns the 20 most recent tweets of the authenticated user that have been retweeted by others.

# API.mentions_timeline([since_id][, max_id][, count])
# Returns the 20 most recent mentions, including retweets.

# API.get_status(id[, trim_user][, include_my_retweet][, include_entities][, include_ext_alt_text][, include_card_uri])
# Returns a single status specified by the ID parameter.

