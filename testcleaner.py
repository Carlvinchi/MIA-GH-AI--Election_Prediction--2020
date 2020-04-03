import tweepy
import cred
import tweets_analyser
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


auth = tweepy.OAuthHandler(cred.CONSUMER_KEY, cred.CONSUMER_SECRET) 
auth.set_access_token(cred.ACCESS_TOKEN, cred.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)
npp_keywords = '#nana akuffo addo OR #npp OR #bawumia OR #president of ghana OR #vice president of Ghana OR #ministers of Ghana OR #nana akuffo addo led administration OR #sitting government of ghana'
query = '#bawumia OR #mahama OR #nana addo OR #npp'
#["asiedu nketia"]
start_date = '2020-03-24'
# Language code (follows ISO 639-1 standards)
language = "en"

if __name__ == "__main__":
    new_entry = []
    filtered = []
    for page in tweepy.Cursor(api.search,q=query,count=100, include_rts=False, since=start_date,tweet_mode='extended').pages(30):
       for status in page:
          status = status._json
          new_entry+=[status]

    df = tweets_analyser.tweets_dataframe(new_entry)
    #print(df.head(60))
    
    
    #df.plt.bar()
    #plt.show(block=True)
    #time_likes = pd.Series(data=df['likes'].values,index=df['date'])
    #time_likes.plot(figsize=(16, 4),label="likes", legend=True)
   #a simple graph
    time_sentiment = pd.Series(data=df['avg_sentiment'].values,index=df['date'])
    time_sentiment.plot(figsize=(16, 4),label="sentiments_ndc", legend=True)
    plt.show()
    #print(np.max(df['likes']))
    
