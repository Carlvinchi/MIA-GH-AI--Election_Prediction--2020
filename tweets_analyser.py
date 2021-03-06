import os
import pandas as pd
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
import data_cleaner
import tweets_analyser
import preprocessor

# function for checking sentiment with Vader library
def sentiment_checker(cleaned_tweet):
   
   analyzer = SentimentIntensityAnalyzer()
   score = analyzer.polarity_scores(cleaned_tweet)
   #polarityScore = (str(score["compound"]))
   return score

# function for checking sentiment with TextBlob library
def sentiment_checker2(cleaned_tweet):
    score_list = []
    pos = 0
    neg = 0
    neu = 0
    blob = TextBlob(cleaned_tweet)
    Sentiment = blob.sentiment
    polarity = Sentiment.polarity
    if polarity > 0:
        pos = polarity
    elif polarity < 0:
        neg = polarity
    else:
        neu = polarity

    subjectivity = Sentiment.subjectivity
    score_list = [pos,neg,neu,subjectivity]
    return score_list

# function for putting data into data frame
def tweets_dataframe(new_entry):
    length_of_entry = len(new_entry)-1
    print(length_of_entry)
    #print(new_entry[0]['full_text'])
    COLS = ['tweets']
    df = pd.DataFrame(columns=COLS)
    for x in range(0,length_of_entry):
        text = new_entry[x]['text']
        print("Processed tweets.... ",x)
        #first cleaninig of data
        cleaned_text = preprocessor.preprocess_tweet(text)
        #second cleaninig of data
        filtered_tweet = data_cleaner.preprocess_tweet(cleaned_text)
        feelings = sentiment_checker(filtered_tweet)
        feelings2 = sentiment_checker2(filtered_tweet)
        single = pd.DataFrame(data=[text],columns=COLS)
        single['id'] = np.array([new_entry[x]['id']])
        single['date'] =np.array ([new_entry[x]['created_at']])
        single['source'] =np.array ([new_entry[x]['source']])
        single['likes'] =np.array ([new_entry[x]['favorite_count']])
        single['retweets'] =np.array ([new_entry[x]['retweet_count']])
        single['clean_tweet'] =np.array ([filtered_tweet])
        single['sentiment_negative'] =np.array ([feelings['neg'] - feelings2[1]])
        single['sentiment_positive'] =np.array ([feelings['pos'] + feelings2[0]])
        single['sentiment_neutral'] =np.array ([feelings['neu'] + feelings2[2]])
        single['subjectivity'] =np.array ([feelings2[3]])
        
        df = df.append(single,ignore_index=True)
    return df