import tweepy
import os.path
import sys
import jsonpickle
import tweets_analyser
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import twitter_credentials
import calendar
import time
 

# Replace the API_KEY and API_SECRET with your application's key and secret.
API_KEY = twitter_credentials.CONSUMER_KEY
API_SECRET = twitter_credentials.CONSUMER_SECRET
auth = tweepy.AppAuthHandler(API_KEY, API_SECRET)

api = tweepy.API(auth, wait_on_rate_limit=True,
                 wait_on_rate_limit_notify=True)

if (not api):
    print("Can't Authenticate")
    sys.exit(-1)

searchQuery = 'akuffo addo'  # this is what we're searching for
maxTweets =10000000   #Some arbitrary large number
tweetsPerQry = 100  # this is the max the API permits
fName = 'Tweets_test/NPP_tweets.csv'  # We'll store the tweets in a text file.
fileName = 'NPP_tweetsaddo_data.csv'
# If results from a specific ID onwards are reqd, set since_id to that ID.
# else default to no lower limit, go as far back as API allows
sinceId = None


# If results only below a specific ID are, set max_id to that ID.
# else default to no upper limit, start from the most recent tweet matching the search query.
max_id = -1

tweetCount = 0
new_entry = []
print("Downloading max {0} tweets".format(maxTweets))
with open(fName, 'a') as f:
    while tweetCount < maxTweets:
        try:
            if (max_id <= 0):
                if (not sinceId):
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry)
                else:
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                            since_id=sinceId)
            else:
                if (not sinceId):
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                            max_id=str(max_id - 1))
                else:
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                            max_id=str(max_id - 1),
                                            since_id=sinceId)
            if not new_tweets:
                print("No more tweets found")
                break
            for tweet in new_tweets:
                status = tweet._json
                new_entry+=[status]
                #f.write(jsonpickle.encode(tweet._json, unpicklable=False) +
                        #'\n')
            tweetCount += len(new_tweets)
            print("Downloaded {0} tweets".format(tweetCount))
            max_id = new_tweets[-1].id
        except tweepy.TweepError as e:
            # Just exit if any error
            print("some error : " + str(e))
            break

print("Downloaded {0} tweets ".format(tweetCount))

df = tweets_analyser.tweets_dataframe(new_entry)
file_exists = os.path.isfile(fileName)

if file_exists:
    with open(fileName, 'a', encoding='utf-8') as f:
        df.to_csv(f, mode='a', index=False, encoding="utf-8")
else:
    f= open(fileName,"a+")
    f.close()
    with open(fileName, 'a', encoding='utf-8') as f:
        df.to_csv(f, mode='a', index=False, encoding="utf-8")

print("Processed {0} tweets and saved successfully ".format(tweetCount))
print("Plotting graphs .....")
sum_df_columns = df.sum(axis=0)
graphs = {}
graphs = {'sentiments_positive':sum_df_columns['sentiment_positive'],'sentiments_negative':sum_df_columns['sentiment_negative']}
plt.bar(graphs.keys(), graphs.values())
plt.title('A Plot of Sentiments base on Nana Addo tweet data')
plt.xlabel('Sentiments')
plt.ylabel('values')
graphName = "graph-" + str(calendar.timegm(time.gmtime())) + ".png"
plt.savefig(graphName)
plt.show()
#print(sumdf)
#print(df.head(5))

