import pandas as pd
import re
import utilities as ut
# coding=gbk 

# all_tweets = pd.read_json("gg2018.json")
host = ""
host_dict = {}
res_dict = {}
award_presenters = {}
reactions = ["mad", "upset", "happy", "sad", "good", "bad", "funny", "cool", "awful", "terrible"]
reax_dict = {"host" : {}, "nominees" : {}, "winners": {}, "presenters" : {}}
stopword_in_awardname = ["-", "by", "an", "a", "or", "for", "any", "in", "Best", "Performance"]
noise_words = ['TV Movie', 'Limited Series', 'Three Billboards', 'Film Drama', 'TV Comedy', 'Film Drama', 'Film Original','TV Drama', 'TV Supporting']

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
    if "s monologue" in tweet_text:
        regex_match = re.search("[A-Z][a-z]* [A-Z][a-z]*", tweet_text)

        if regex_match:
            probable_name = regex_match.group(0)
            
            if "The " not in probable_name:
                if probable_name in host_dict.keys():
                    host_dict[probable_name] += 1
                    getReactions("host", probable_name, tweet_text, False)
                else:
                    host_dict[regex_match.group(0)] = 1
                    getReactions("host", probable_name, tweet_text, True)
                    


presenter_keyword = ["will be presenting", "will present", "presenting", "to present", "presents", "present"]
def getPresenter(tweet_text):
    # award name is after, and presenter is before
    presenterPart = ""
    awardPart = ""
    if "presented by" in tweet_text:
        splitTweet = tweet_text.split('presented by')
        presenterPart = splitTweet[1]
        awardPart = splitTweet[0]
        extractPresenter(presenterPart, awardPart)
    else:
        for i in presenter_keyword:
            if i in tweet_text:
                splitTweet = tweet_text.split(i)
                presenterPart = splitTweet[0]
                awardPart = splitTweet[1]
                extractPresenter(presenterPart, awardPart)
                break
    
    
def extractPresenter(presenterPart, awardPart):
    # remove special charactors will effect word processing
    presenterPart = presenterPart.replace('&amp;', 'and')
    awardPart = awardPart.replace('/', ' ')
    pa = re.compile("[A-Z][a-zA-Z-]* [A-Z][a-zA-Z-]*")
    presenter = pa.findall(presenterPart)
    
    # remove noise word from presenter candidates list
    for i in presenter:
        if i in noise_words:
            presenter.remove(i)
            
    weightCal = {}
    for i in award_presenters.keys():
        weightCal[i] = 0
        awardWords = award_presenters[i][0]
        for j in awardWords:
            if j in awardPart:
                weightCal[i] += 1
        weightCal[i] = weightCal[i] / (1.0 * len(awardWords))
    sort = sorted(weightCal.items(), key=lambda e:e[1], reverse=True)
    if len(presenter) != 0:
        for i in sort:
            relativeAward = i[0]
            if award_presenters[relativeAward][1] == "":
                award_presenters[relativeAward][1] = presenter
                award_presenters[relativeAward][2] = i[1]
                break
            elif i[1] > award_presenters[relativeAward][2]:
                test = award_presenters[relativeAward]
                award_presenters[relativeAward][1] = presenter
                award_presenters[relativeAward][2] = i[1]
                break;


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
            winner, award= ut.splitWord(award_name)
            winner = ut.filterBracket(winner)
            award = ut.filterHash(award)
            
            if winner in res_dict.keys():
                # getReaction doesn't actually get anything for this because of how the tweet are filtered, but that's ok bc we use it later
                getReactions("winners", winner, tweet_text, False) 
                res_dict[winner] = ut.getBetterName(res_dict[winner], award)
            else:
                res_dict[winner] = award
                # getReaction doesn't actually get anything for this because of how the tweet are filtered
                getReactions("winners", winner, tweet_text, True)


if __name__ == '__main__':
    all_tweets = pd.read_json("gg2018.json")
    """loop into each line of tweet"""
    for index, row in all_tweets.iterrows():
        tweet_text = row["text"]
        getHost(tweet_text)
        getAwardsAndWinners(tweet_text)

    host = max(host_dict, key=host_dict.get)
    print("The host is ", host)
    print("reaction is: ", max(reax_dict["host"][host], key= reax_dict["host"][host].get));
    print()
    
    
    # make a new dic to store award to presenter mapping
    # get all award name from winner to award dic    
    for i in res_dict.keys():
        awardName = res_dict[i]
        award_presenters[awardName] = []
        award_presenters[awardName].append(ut.generateComparasionDictionary(awardName, stopword_in_awardname))  
        award_presenters[awardName].append("")
        award_presenters[awardName].append(-1)
    
    # Go back through all of the tweets again and find reactions for each award/winner
    
    for index, row in all_tweets.iterrows():
        tweet_text = row["text"]
        getPresenter(tweet_text)
        
        # now go through and find the reactions''
        for i in res_dict.keys():
            
            if i in tweet_text:
                getReactions("winners", i, tweet_text, False)

    for i in res_dict.keys():
        #print("Award name: " + str(res_dict[i]) + "   winner is: " + str(i) + " reaction: " + str( max(reax_dict["winners"][i], key= reax_dict["winners"][i].get)))
        print("Award name: " + str(res_dict[i]))
        print("Winner is: " + str(i))
        print("Presenter is: " + str(award_presenters[res_dict[i]][1]))
        print("Reaction is: " + str( max(reax_dict["winners"][i], key= reax_dict["winners"][i].get)))
        print("")
        