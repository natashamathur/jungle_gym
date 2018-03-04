def common_word(x):
    d = {}
    x = x.split()
    for word in x:
        if word not in d.keys():
            d[word] = 1
        else:
            d[word] += 1

    k = list(k.keys())
    v = list(v.values())
    max = k[v.index(max(v))]
            
    return max

x = "“The sovereigns? I do not speak of Russia,” said the vicomte, polite but hopeless: “The sovereigns, madame... What have they done for Louis XVII, for the Queen, or for Madame Elizabeth? Nothing!” and he became more animated. “And believe me, they are reaping the reward of their betrayal of the Bourbon cause. The sovereigns! Why, they are sending ambassadors to compliment the usurper.”"





