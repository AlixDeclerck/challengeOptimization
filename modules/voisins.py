import random
from .SolConfig import SolConfig

def permutRing(ring, permutations=1):
    newRing = ring.copy()

    if len(newRing) >= 2:
        for i in range(permutations):
            pos1 = random.randint(1, len(newRing)-1)
            pos2 = random.randint(1, len(newRing)-1)
            temp = newRing[pos1]
            newRing[pos1] = newRing[pos2]
            newRing[pos2] = temp

    return newRing

def permutInRing(instance, permutations=1):
    newRing = instance.getRing()

    newRing = permutRing(newRing, permutations=permutations)

    return SolConfig(newRing)


def addSummit(ring, summitsAccount, summitsToAdd=1):
    newRing = ring.copy()

    actualStars = [i for i in range(2, summitsAccount+1) if i not in newRing]

    for i in range(summitsToAdd):
        if len(actualStars) != 0:
            newRing.insert(random.randint(1, len(newRing)), actualStars.pop(random.randint(0, len(actualStars)-1)))

    return newRing

def addSummitInRing(instance, summitsAccount, summitsToAdd=1):
    newRing = instance.getRing()

    newRing = addSummit(newRing, summitsAccount=summitsAccount, summitsToAdd=summitsToAdd)

    return SolConfig(newRing)


def removeSummit(ring, summitsToRemove=1):
    newRing = ring.copy()

    for i in range(summitsToRemove):
        if(len(newRing) > 1):  # Le dépôt doit rester absolument
            newRing.pop(random.randint(1, len(newRing)-1))

    return newRing

def removeSummitOfRing(instance, summitsToRemove=1):
    newRing = instance.getRing()

    newRing = removeSummit(newRing, summitsToRemove=summitsToRemove)

    return SolConfig(newRing)

def elementaryNeighbours(subject, summitsAccount, numberOfNeighbours=20, neighboursMaxDistance=1):
    newSubjects = []

    for i in range(numberOfNeighbours):
        j = random.randint(1, 3)
        dist = random.randint(1, neighboursMaxDistance)

        if j == 1:
            newSubject = permutInRing(subject, permutations=dist)
        elif j == 2:
            newSubject = addSummitInRing(subject, summitsAccount=summitsAccount, summitsToAdd=dist)
        else:
            newSubject = removeSummitOfRing(subject, summitsToRemove=dist)

        newSubjects.append(newSubject)

    return newSubjects


def ringCost(ring, ringWeights):
    ring_cost = 0

    lastSummit = 1
    for summit in range(1, len(ring)):
        ring_cost += ringWeights[lastSummit-1, summit-1]
        lastSummit = summit
    ring_cost += ringWeights[ring[-1]-1, 1-1]

    return ring_cost

def salesManProblem(ring, ring_weights, maxIterWithoutImprove=25):
    subject = ring.copy()

    counterWithoutImprove = 0
    while counterWithoutImprove < maxIterWithoutImprove:

        newSubject = permutRing(subject, random.randint(1, 3))

        if ringCost(newSubject, ring_weights) < ringCost(subject, ring_weights):
            subject = newSubject
            counterWithoutImprove = 0
        else:
            counterWithoutImprove += 1

    return subject


def salesManInRingNeighbours(subject, summitsAccount, numberOfNeighbours=20, neighboursMaxDistance=1):
    newSubjects = []

    for i in range(numberOfNeighbours):
        j = random.randint(1, 3)
        dist = random.randint(1, neighboursMaxDistance)

        ring = subject.getRing()

        if j == 1:
            newRing = permutRing(ring, permutations=dist)
        elif j == 2:
            newRing = addSummit(ring, summitsAccount=summitsAccount, summitsToAdd=dist)
        else:
            newRing = removeSummit(ring, summitsToRemove=dist)


        newRing = salesManProblem(newRing, SolConfig.ring_weights)
        newSubjects.append(SolConfig(newRing))

    return newSubjects
