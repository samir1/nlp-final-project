import json
import ast
import argparse
from google.cloud import language

data = []

language_client = language.Client()

with open('tweets_with_location_copy_monday.txt') as f:
    for line in f:
        data.append(ast.literal_eval(line))
        # print(data[len(data)-1]['text'])
        # if 'place' in data[len(data)-1] and data[len(data)-1]['place']:
        #     print(data[len(data)-1]['place']['full_name'])
        # elif 'coordinates' in data[len(data)-1] and data[len(data)-1]['coordinates']:
        #     print(data[len(data)-1]['coordinates'])
        if len(data) == 10:
            break

for tweet in data:
    text = tweet['text']

    document = language_client.document_from_text(text)

    sentiment = document.analyze_sentiment().sentiment

    print('Text: {}'.format(text))
    print('Sentiment: {}, {}'.format(sentiment.score, sentiment.magnitude))
    print()
