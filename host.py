import pandas as pd
import re

all_tweets = pd.read_json("gg2018.json")
monologue  = all_tweets[all_tweets['text'].str.contains("s monologue ")]

host_dict = {}

for index, row in monologue.iterrows():
    tweet_text = row["text"]
    # print(tweet_text)
    regex_match = re.search("[A-Z][a-z]* [A-Z][a-z]*", tweet_text)
    
    if regex_match:
        if "The " not in regex_match.group(0):
            if regex_match.group(0) in host_dict.keys():
                host_dict[regex_match.group(0)] += 1
            else:
                host_dict[regex_match.group(0)] = 1
            #print(regex_match.group(0))

print(max(host_dict, key=host_dict.get))