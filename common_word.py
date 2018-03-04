def common_words(x, remove_stop_words = True):
    '''
    Takes in a .txt file and returns the most commonly used word. 
    '''

    x = open(x, 'r')
    x = x.read()
    lx = x.lower().split()

    STOP_WORDS = ["a", "an", "the", "this", "that", "of", "for", "or", 
         "and", "on", "to", "be", "if", "we", "you", "in", "is", 
         "at", "it", "rt", "mt", "with"]

    if remove_stop_words:
        lx = [w for w in lx if w not in STOP_WORDS]
    
    d = {}
    for word in lx:
        if word not in d.keys():
            d[word] = 1
        else:
            d[word] += 1

    k = list(d.keys())
    v = list(d.values())
    most_common = sorted(d, key = d.get, reverse=True)[:5]
            
    return "The five most common words are: " + ( ", ".join( repr(e) for e in most_common))







