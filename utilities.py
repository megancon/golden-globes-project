import re



def wordLen(s):
    return len([i for i in s.split(' ') if i])


def splitWord(s):
    candidates = s.split('-')
    winner = candidates[0]
    award = candidates[1]
    if len(candidates) > 2:
        award += "-"
        award += candidates[2]
        
    return winner.strip(), award.strip()


def getBetterName(s, t):
    if (len(s) > len(t)):
        return s
    
    return t
	
	
def filterBracket(inputStr):
    replacedStr = re.sub(r" \(.+?\)", "", inputStr, flags=re.I)
    return replacedStr

def filterHash(inputStr):
    replacedStr = re.sub(r" #.*", "", inputStr, flags=re.I)
    return replacedStr

def flipWinnerAndAwardName(res_dic):
    res = {}
    for i in res.keys():
        awardName = res[i]
        winner = i
        res[awardName] = winner
        
    return res


