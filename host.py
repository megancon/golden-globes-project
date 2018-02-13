import pandas as pd
import re
import utilities as ut

all_tweets = pd.read_json("gg2018.json")
host = ""
host_dict = {}
res_dict = {}
test = {}
test_counter = 0


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


def getPresenter(tweet_text):
    return


def getAttendance(tweet_text):
    return


def getAwardsAndWinners(tweet_text):
    regex_match = re.search("(?<=Congratulations to ).*(?=[\(\u2026])", tweet_text)
    global test_counter

    if regex_match:
        # get award name and do some standardizing
        award_name = regex_match.group(0)
        award_name = re.sub(r'(television\s+series)|(tv\s+series)', 'TV Series', award_name, flags=re.IGNORECASE)
        
        if ut.wordLen(award_name) <= 4:
            return
        if "-" not in award_name:
            return
        regex_match = re.search("^[A-Z].*- Best.*", award_name)
        if regex_match:  
            award_name = regex_match.group(0)
            award, winner = ut.splitWord(award_name)
            
            if winner in res_dict.keys():
                res_dict[winner] = ut.getBetterName(res_dict[winner], award)
            else:
                res_dict[winner] = award


if __name__ == '__main__':
    all_tweets = pd.read_json("gg2018.json")
    """loop into each line of tweet"""
    for index, row in all_tweets.iterrows():
        tweet_text = row["text"]
        getHost(tweet_text)
        getAwardsAndWinners(tweet_text)
        """TODO more functions need to be called here"""

    host = max(host_dict, key=host_dict.get)
    print(host)

    for i in res_dict.keys():
        print(str(i) + "   winner is: " + str(res_dict[i]))