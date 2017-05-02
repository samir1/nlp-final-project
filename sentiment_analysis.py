import json
import ast
import sys
import argparse
import us
import csv
import time
from google.cloud import language

data = {}
language_client = language.Client()

def get_tweet_state(tweet):
    if 'place' in tweet and tweet['place']:
        place = tweet['place']
        if place['country_code'] == 'US':
            state_abbr = place['full_name'][place['full_name'].rfind(',')+1:].strip()
            if us.states.lookup(state_abbr):
                # state = us.states.lookup(state_abbr)
                # return str(state)
                return state_abbr
            else:
                return None

def sentiment_for_tweet(tweet):
    text = tweet['text']
    document = language_client.document_from_text(text)
    document.language = 'en'
    sentiment = document.analyze_sentiment().sentiment
    # print('Text: {}'.format(text))
    # print('Sentiment: {}, {}'.format(sentiment.score, sentiment.magnitude))
    final_score = sentiment.score * sentiment.magnitude
    return final_score

def generate_average(data):
    for key, value in data.items():
        tweet_count = value[0]
        total_sent = value[1]
        avg = total_sent/tweet_count
        if len(value) > 2 and value[2]:
            value[2] = avg
        else:
            value.append(avg)
    return data

def normalize_average(data):
    min_val = float('inf')
    max_val = float('-inf')
    for key, value in data.items():
        if value[2] < min_val:
            min_val = value[2]
        if value[2] > max_val:
            max_val = value[2]
    if (min_val < float('inf') and min_val != 0) and (max_val > float('-inf') and max_val != 0):
        for key, value in data.items():
            normalized_avg = (2*((value[2] - min_val)/(max_val - min_val)))-1
            if len(value) > 3 and value[3]:
                value[3] = normalized_avg
            else:
                value.append(normalized_avg)
    return data

def write_csv(data):
    with open('data.csv', 'w') as f:
        fieldnames = ['state','num_tweets_from_state','total_sentiment','sentiment_avg','normalized_sentiment_avg']
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for key, value in data.items():
            row = {'state': key}
            row['num_tweets_from_state'] = value[0]


            row['total_sentiment'] = value[1]


            if len(value) > 2:
                row['sentiment_avg'] = value[2]
            else:
                row['sentiment_avg'] = 0


            if len(value) > 3:
                row['normalized_sentiment_avg'] = value[3]
            else:
                row['normalized_sentiment_avg'] = 0

            w.writerow(row)

with open('tweets_with_location_sun.txt') as f:
    count = 0
    for line in f:
        tweet = ast.literal_eval(line)
        state = get_tweet_state(tweet)
        if state:
            sentiment = sentiment_for_tweet(tweet)
            if state in data:
                data[state][0] = data[state][0] + 1
                data[state][1] = data[state][1] + sentiment
            else:
                data[state] = [1, sentiment]
            data = generate_average(data)
            data = normalize_average(data)
            write_csv(data)
            count += 1
        if count == 999:
            count = 0
            print('sleeping for 101 seconds')
            time.sleep(101)
            print('starting again')

generate_average(data)

normalize_average(data)

print(data)

print("writing csv")
write_csv(data)
