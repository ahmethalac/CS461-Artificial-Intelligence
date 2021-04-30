import nltk
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


stopWords = set(stopwords.words('english'))

"""This function creates tokens to be searched on the web-sites"""

def getSearchedTokens(clue):
    
    punctuationFree = clue.translate(str.maketrans('', '', string.punctuation))

    tokens = word_tokenize(punctuationFree)             # split the punctiuation free clue to tokens (list)
    tokens = [w for w in tokens if not w in stopWords]  # remove stopwordss from tokens

    tokenNum = len(tokens)

    # for i in range(tokenNum):
    #     if i != tokenNum - 1:
    #         tokens.append(tokens[i] + " " + tokens[i + 1])
    # tokens.append(clue)

    for i in range(tokenNum):
        new_token = tokens[i]
        for j in range(i+1,tokenNum):
            new_token = new_token + " " + tokens[j]
            tokens.append(new_token)

    return tokens