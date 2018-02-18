import pandas as pd
import re
import utilities as ut

# all_tweets = pd.read_json("gg2018.json")
host = ""
host_dict = {}
res_dict = {}
test = {}
test_counter = 0

reactions = ["mad", "upset", "happy", "sad", "good", "bad", "funny", "cool", "awful", "terrible"]
reax_dict = {"host" : {}, "nominees" : {}, "winners": {}, "presenters" : {}}


def getReactions(category, name, tweet, isnew):
    if isnew:
        reax_dict[category][name] = {key: 0 for key in reactions}
        
        for reaction in reactions:
            if reaction in tweet:
                reax_dict[category][name][reaction] = 1
    
    else:
         for reaction in reactions:
            if reaction in tweet:
                reax_dict[category][name][reaction] += 1
    


def getHost(tweet_text):
    """TODO more phases here, not just only s monologue"""
    if "s monologue" in tweet_text:
        regex_match = re.search("[A-Z][a-z]* [A-Z][a-z]*", tweet_text)
        """TODO more regex match here"""

        if regex_match:
            probable_name = regex_match.group(0)
            
            if "The " not in probable_name:
                if probable_name in host_dict.keys():
                    host_dict[probable_name] += 1
                    getReactions("host", probable_name, tweet_text, False)
                else:
                    host_dict[regex_match.group(0)] = 1
                    getReactions("host", probable_name, tweet_text, True)
                    


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
                # getReaction doesn't actually get anything for this because of how the tweet are filtered, but that's ok bc we use it later
                getReactions("winners", award, tweet_text, False) 
                res_dict[winner] = ut.getBetterName(res_dict[winner], award)
            else:
                res_dict[winner] = award
                # getReaction doesn't actually get anything for this because of how the tweet are filtered
                getReactions("winners", award, tweet_text, True)


if __name__ == '__main__':
    all_tweets = pd.read_json("gg2018.json")
    """loop into each line of tweet"""
    for index, row in all_tweets.iterrows():
        tweet_text = row["text"]
        getHost(tweet_text)
        getAwardsAndWinners(tweet_text)
        """TODO more functions need to be called here"""

    host = max(host_dict, key=host_dict.get)
    print("The host is ", host, "reaction: ", max(reax_dict["host"][host], key= reax_dict["host"][host].get) )
    
    # Go back through all of the tweets again and find reactions for each award/winner
    
    for index, row in all_tweets.iterrows():
        tweet_text = row["text"]
        
        # now go through and find the reactions''
        for i in res_dict.keys():
            
            if res_dict[i].split("(")[0] in tweet_text:
                getReactions("winners", res_dict[i], tweet_text, False)
    
    
    for i in res_dict.keys():
        print(str(i) + "   winner is: " + str(res_dict[i]) + " reaction: " + str( max(reax_dict["winners"][res_dict[i]], key= reax_dict["winners"][res_dict[i]].get)))