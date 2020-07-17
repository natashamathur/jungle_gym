# https://www.hackerrank.com/challenges/determining-dna-health/problem

# input provided by prompt
n = 6
g = " a b c aa d b"
h = [1, 2, 3, 4, 5, 6]
s = 3
l1 = (1, 5, "caaab")
l2 = (0, 4, "xyz")
l3 = (2, 4, "bcdybc")

'''
CODE STARTS
'''
def determine_dna_health(g, h, genes):

    all_gg= g.split()
    final = []

    # make gene dictionary
    gene_dict= {}
    for i in all_gg:
        if i not in gene_dict.keys():
            gene_dict[i] = [h[x] for x,y in enumerate(all_gg) if y == i]

    for gene in genes: 

        # get list of healthy strands for this gene
        healthy = []
        g = gene[2]
        for i in range(0, len(g)):
            if i >= gene[0] and i <= gene[1]:
                healthy.append(all_gg[i])
        max_strand = len(max(healthy, key=len))

        total = 0
        for st in range(len(g)):
            if g[st] in healthy:
                t = g[st]
                total += sum(gene_dict[t])
            if st < len(g)-1 and g[st:st+max_strand] in healthy:
                t = g[st:st+max_strand]
                total += sum(gene_dict[t])

        final.append(total)

    output = min(final), max(final)
    return output

# generate output
genes = [l1, l2, l3]
print(determine_dna_health(g,h, genes))

# https://www.hackerrank.com/challenges/word-order/problem

def word_order(input):
    num_words = len(input)
    wordd = {}

    for w in input:
        if w not in wordd.keys():
            wordd[w] = 1
        else:
            wordd[w] += 1

    print(len(wordd.keys()))
    print(list(wordd.values()))

input = ['cat', 'cat', 'dog', 'eagle']
word_order(input)
