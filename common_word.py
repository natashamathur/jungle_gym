def common_words(x):
    '''
    Takes in a .txt file and returns the most commonly used word. 
    '''

    x = open(x, 'r')
    x = x.read()
    lx = x.split()
    
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







