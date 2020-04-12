import os.path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import calendar
import time
import GetOldTweets3 as got
import  tweets_analyser

#graphName = "graph-" + str(date.today()) + ".txt"
fileName = 'NPP_hist_data.csv'
def get_tweets():
    tweetCriteria = got.manager.TweetCriteria().setQuerySearch('npp') \
        .setSince("2019-12-01") \
        .setUntil("2020-03-1") \
        .setMaxTweets(500)
    tweets = got.manager.TweetManager.getTweets(tweetCriteria)
    tweet_id = [tweet.id for tweet in tweets]
    tweet_text = [tweet.text for tweet in tweets]
    tweet_date = [tweet.date for tweet in tweets]
    tweet_retweets = [tweet.retweets for tweet in tweets]
    tweet_likes = [tweet.favorites for tweet in tweets]
    getdf = tweets_analyser.tweets_dataframe(tweet_id, tweet_text,tweet_date, tweet_retweets, tweet_likes)
    return getdf
    #retweets(int)
    #favorites(int)


if __name__=="__main__":
    df = get_tweets()
    
    
    file_exists = os.path.isfile(fileName)

    if file_exists:
        with open(fileName, 'a', encoding='utf-8') as f:
            df.to_csv(f, mode='a', index=False, encoding="utf-8")
    else:
        f= open(fileName,"a+")
        f.close()
        with open(fileName, 'a', encoding='utf-8') as f:
            df.to_csv(f, mode='a', index=False, encoding="utf-8")

    
    print("Plotting graphs .....")
    sum_df_columns = df.sum(axis=0)
    graphs = {}
    graphs = {'sentiments_positive':sum_df_columns['sentiment_positive'],'sentiments_negative':sum_df_columns['sentiment_negative']}
    plt.bar(graphs.keys(), graphs.values())
    plt.title('A Plot of Sentiments base on NPP tweet data')
    plt.xlabel('Sentiments')
    plt.ylabel('values')
    graphName = "graph-" + str(calendar.timegm(time.gmtime())) + ".png"
    plt.savefig(graphName)
    plt.show()