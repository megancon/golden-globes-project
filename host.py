import pandas as pd
import re

all_tweets = pd.read_json("gg2018.json")
host = ""
host_dict = {}


def getHost(tweet_text):
    """TODO more phases here, not just only s monologue"""
    if "s monologue" in tweet_text:  
        regex_match = re.search("[A-Z][a-z]* [A-Z][a-z]*", tweet_text)
        """TODO more regex match here"""
    
        if regex_match:
            if "The " not in regex_match.group(0):
                if regex_match.group(0) in host_dict.keys():
                    host_dict[regex_match.group(0)] += 1
                else:
                    host_dict[regex_match.group(0)] = 1

def getAwardWinner(tweet_text):
    return

def getpresenter(tweet_text):
    return

def getAttendance(tweet_text):
    return

def main():
    all_tweets = pd.read_json("gg2018.json")
    """loop into each line of tweet"""
    for index, row in all_tweets.iterrows():
        tweet_text = row["text"]
        getHost(tweet_text)
        """TODO more functions need to be called here"""
        
        
    host = max(host_dict, key=host_dict.get)
    print (host)
    
    
    
main()
        