import random

"""
Allow the user to shuffle solutions into a dictionnary to simulate migrations
"""
def shuffle(d, numberOfMigrations):
    d = d.copy()

    for i in range(numberOfMigrations):
        key1 = random.choice(list(d.keys()))
        key2 = random.choices(list(d.keys()), weights=[len(d[key]) for key in list(d.keys())])[0]
        while len(d[key2]) == 0 and key2 != key1:
            key1 = random.choice(list(d.keys()))
            key2 = random.choices(list(d.keys()), weights=[len(d[key]) for key in list(d.keys())])[0]
        d[key1].append(d[key2].pop(random.randint(0, len(d[key2])-1)))

    return d

def partialLocalSearch(subjectsList, neighboursFunction, functionKargs, msgHeader=""):
    subjectsList = subjectsList.copy()
    maxIterWithoutImprove = 20

    for i, subject in enumerate(subjectsList):

        counterWithoutImprove = 0
        while counterWithoutImprove < maxIterWithoutImprove:
            newSubjects = neighboursFunction(subject, **functionKargs)
            newSubjects.append(subject)
            bestNewSubject = min(newSubjects, key=lambda item: item.getCost())

            if bestNewSubject.getCost() < subject.getCost():
                subject = bestNewSubject
                counterWithoutImprove = 0
            else:
                counterWithoutImprove += 1

        print(f"{msgHeader}{i+1}/{len(subjectsList)} -> best = {subject.getCost()}")
        subjectsList[i] = subject

    return subjectsList
