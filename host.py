import pandas as pd
import re

all_tweets = pd.read_json("gg2018.json")
host = ""
host_dict = {}
awards_dict = {}


def wordLen(s):
    return len([i for i in s.split(' ') if i])


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


def getPresenter(tweet_text):
    return


def getAttendance(tweet_text):
    return


def getAwards(tweet_text):
    regex_match = re.search("\"Best [A-Za-z -]*\"", tweet_text)

    if regex_match:
        # get award name and do some standardizing
        award_name = regex_match.group(0)
        award_name = re.sub(r'(television\s+series)|(tv\s+series)', 'TV Series', award_name, flags=re.IGNORECASE)
        
        if wordLen(award_name) <= 4:
            return
        if award_name in awards_dict.keys():
            awards_dict[award_name] += 1
        else:
            awards_dict[award_name] = 1


if __name__ == '__main__':
    all_tweets = pd.read_json("gg2018.json")
    """loop into each line of tweet"""
    for index, row in all_tweets.iterrows():
        tweet_text = row["text"]
        getHost(tweet_text)
        getAwards(tweet_text)
        """TODO more functions need to be called here"""

    host = max(host_dict, key=host_dict.get)
    print(host)

    for i in awards_dict:
        print(i)
