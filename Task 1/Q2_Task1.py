from __future__ import division
import collections

lines = open('input.txt').read().splitlines()

for x in range(len(lines)):
    lines[x] = lines[x].split(' ')

print lines

# P is the set of all pages; |P| = N
# S is the set of sink nodes, i.e., pages that have no out links
# M(p) is the set of pages that link to page p
# L(q) is the number of out-links from page q
# d is the PageRank damping/teleportation factor; use d = 0.85 as is typical

# populating P

P = []

for x in range(len(lines)):
    P.append(lines[x][0])

print P

# populating M

M = collections.defaultdict(list)

for x in range(len(lines)):
    for y in range(1, len(lines[x])):
        M[lines[x][0]].append(lines[x][y])

print M

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

print L
print 'printing S...'
print S

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

print newPR

count = 0

while PR != newPR:

    count += 1

    for x in range(len(P)):
        PR[P[x]] = newPR[P[x]]

    sinkPR = 0
    for x in range(len(S)):    # calculate total sink PR
        sinkPR += PR[S[x]]

    for x in range(len(P)):
        newPR[P[x]] = (1 - d) / N   # teleportation
        newPR[P[x]] += d * sinkPR / N   # spread remaining sink PR evenly
        for y in range(len(M[P[x]])):    # pages pointing to p
            newPR[P[x]] += d * PR[M[P[x]][y]] / L[M[P[x]][y]]   # add share of PageRank from in-links

    if count == 1 or count == 10 or count == 100:
        print newPR

print PR
print newPR
print count
