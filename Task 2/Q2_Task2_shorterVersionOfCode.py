from __future__ import division
import collections
import math

lines = open('wt2g_inlinks').read().splitlines()

P = []
M = collections.defaultdict(list)
L = {}
S = []
d = 0.85
PR = {}
newPR = {}
perplexity = []
convergence = False
count = 0

for x in range(len(lines)):
    lines[x] = lines[x].split(' ')
    lines[x] = filter(None, lines[x])
    P.append(lines[x][0])   # populating P
    for y in range(1, len(lines[x])):
        M[lines[x][0]].append(lines[x][y])  # populating M
    L[lines[x][0]] = 0  # initialising L

N = len(P)

for x in range(len(lines)):
    for y in range(1, len(lines[x])):
        L[lines[x][y]] += 1     # populating L

for x in range(len(lines)):
    if L[lines[x][0]] == 0:
        S.append(lines[x][0])   # populating S

for x in range(len(P)):
    PR[P[x]] = 0
    newPR[P[x]] = 1/N   # initial value

for x in range(4):
    perplexity.append(0)

while convergence == False:

    for x in range(len(P)):
        PR[P[x]] = newPR[P[x]]

    entropyOfDistribution = 0

    for x in range(len(P)):
        entropyOfDistribution += -newPR[P[x]]*math.log(newPR[P[x]], 2)

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

print count

sortedCollection = sorted(PR, key=PR.get, reverse=True)

f = open('sortedCollection.txt', 'w')
f.write(str(sortedCollection))
f.close()

for x in range(10):
    print sortedCollection[x],
    print ':',
    print PR[sortedCollection[x]]
