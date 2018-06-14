import sys
from string import punctuation

def strip_punctuation(s):
    
    return ''.join(c for c in s if c not in punctuation)

def common_words(x, n=5, more_stops = [], remove_stop_words = True):
    '''
    Takes in a .txt file or a string and returns the most commonly used word. 
    '''

    if type(x) is not str:
        x = open(x, 'r', encoding = 'latin-1')
        x = x.read()

    x = strip_punctuation(x)
    lx = x.lower().split()
    
    STOP_WORDS = [ "a", "about", "above", "after", "again", "nan", "against", "all", "am", "an", "and", "any", "are", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "could", "did", "do", "does", "doing", "down", "during", "each", "few", "for", "from", "further", "had", "has", "have", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "it", "it's", "its", "itself", "let's", "me", "more", "most", "my", "myself", "nor", "of", "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "she", "she'd", "she'll", "she's", "should", "so", "some", "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too", "under", "until", "up", "very", "was", "we", "we'd", "we'll", "we're", "we've", "were", "what", "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with", "would", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves" ]

    
    if len(more_stops) > 0:
        STOP_WORDS = STOP_WORDS + more_stops
        
    if remove_stop_words:
         lx = [w for w in lx if w not in STOP_WORDS]
    
    d = {}
    for word in lx:
        if word not in d.keys():
            d[word] = 1
        else:
            d[word] += 1

    most_common = sorted(d, key = d.get, reverse=True)[:n]
            
    #print("The " + str(n) + " most common words are: " + ( ", ".join( e for e in most_common)) + ".")
    return most_common

import json

def str_fb_comments(jsonfile):
    '''
    Gets string of all facebook comments from Facebook-provided data. 
    '''

    f = open(jsonfile)
    data = json.load(f)

    comments = []
    for c in range(len(data)):
        try:
            temp = data[c]['data'][0]['comment']['comment']
            comments.append(temp)
        except:
            # ignore comment as this is an attachment, not text
            pass
    
    s = ''
    for c in comments:
        s = s + " " + c

    return s

s = str_fb_comments('comments.json')

print(cw.common_words(s, n=10))

'''
Here are the results for my facebook comments!

The 10 most common words are: not, im, like, just, dont, know, thats, thank, now, can.
'''
