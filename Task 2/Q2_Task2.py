from __future__ import division
import collections
import math

lines = open('wt2g_inlinks').read().splitlines()

for x in range(len(lines)):
    lines[x] = lines[x].split(' ')
    lines[x] = filter(None, lines[x])

# P is the set of all pages; |P| = N
# S is the set of sink nodes, i.e., pages that have no out links
# M(p) is the set of pages that link to page p
# L(q) is the number of out-links from page q
# d is the PageRank damping/teleportation factor; use d = 0.85 as is typical

# populating P

P = []

for x in range(len(lines)):
    P.append(lines[x][0])

# populating M

M = collections.defaultdict(list)

for x in range(len(lines)):
    for y in range(1, len(lines[x])):
        M[lines[x][0]].append(lines[x][y])

# print M

# populating L and S

L = {}

for x in range(len(lines)):
    L[lines[x][0]] = 0

S = []

for x in range(len(lines)):
    for y in range(1, len(lines[x])):
        L[lines[x][y]] += 1

for x in range(len(lines)):
    if L[lines[x][0]] == 0:
        S.append(lines[x][0])

# populating d

d = 0.85

# populating N

N = len(P)

# populating PR

PR = {}
newPR = {}

for x in range(len(P)):
    PR[P[x]] = 0
    newPR[P[x]] = 1/N   # initial value

count = 0

perplexity = []

for x in range(4):
    perplexity.append(0)

convergence = False

while convergence == False:

    for x in range(len(P)):
        PR[P[x]] = newPR[P[x]]

    # calculate entropy

    entropyOfDistribution = 0

    for x in range(len(P)):
        entropyOfDistribution += -newPR[P[x]]*math.log(newPR[P[x]], 2)

    # calculate perplexity

    perp = math.pow(2, entropyOfDistribution)

    perp = int(round(perp))

    print perp

    perplexity[count % 4] = perp

    if perplexity[0] == perplexity[1] == perplexity[2] == perplexity[3]:
        convergence = True
        break

    sinkPR = 0
    for x in range(len(S)):    # calculate total sink PR
        sinkPR += PR[S[x]]

    for x in range(len(P)):
        newPR[P[x]] = (1 - d) / N   # teleportation
        newPR[P[x]] += d * sinkPR / N   # spread remaining sink PR evenly
        for y in range(len(M[P[x]])):    # pages pointing to p
            newPR[P[x]] += d * PR[M[P[x]][y]] / L[M[P[x]][y]]   # add share of PageRank from in-links

    count += 1

# print PR
print count

# sort the collection of web pages

sortedCollection = sorted(PR, key=PR.get, reverse=True)

f = open('sortedCollection.txt', 'w')
f.write(str(sortedCollection))
f.close()

# list top 10 pages sorted by page rank with their page rank values

for x in range(10):
    print sortedCollection[x],
    print ':',
    print PR[sortedCollection[x]]
