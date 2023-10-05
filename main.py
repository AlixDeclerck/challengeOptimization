from modules.readData import readData
from modules.SolConfig import SolConfig
from modules.metaheuristiques import partialLocalSearch, shuffle
from modules.voisins import elementaryNeighbours, salesManProblem, salesManInRingNeighbours
import time

path = "./fichiers/data1.dat"

endMsg = """, ,    ,      ,    ,     ,     ,   ,      ,     ,     ,      ,      ,
,       ,     ,    ,       ,   .____. ,   ,     ,      ,       ,      ,
 ,    ,   ,    ,     ,   ,   , |   :|         ,   , ,   ,   ,       ,
   ,        ,    ,     ,     __|====|__ ||||||  ,        ,      ,      ,
 ,   ,    ,   ,     ,    , *  / o  o \  ||||||,   ,  ,        ,    ,
,   ,   ,         ,   ,     * | -=   |  \====/ ,       ,   ,    ,     ,
   ,  ,    ,   ,           , U==\__//__. \\//    ,  ,        ,    ,
,   ,  ,    ,    ,    ,  ,   / \\==// \ \ ||  ,   ,      ,          ,
 ,  ,    ,    ,     ,      ,|    o ||  | \||   ,      ,     ,   ,     ,
,      ,    ,    ,      ,   |    o ""  |\_|B),    ,  ,    ,       ,
  ,  ,    ,   ,     ,      , \__  --__/   ||  ,        ,      ,     ,
,  ,   ,       ,     ,   ,  /          \  ||,   ,   ,      ,    ,    ,
 ,      ,   ,     ,        |            | ||      ,  ,   ,    ,   ,
,    ,    ,   ,  ,    ,   ,|            | || ,  ,  ,   ,   ,     ,  ,
 ------_____---------____---\__ --_  __/__LJ__---------________-----___"""


if __name__ == '__main__':
    tic = time.time()
    try:
        ring_weights, stars_weights, n = readData(path)
    except:
        ring_weights, stars_weights, n = readData('.'+path)

    kargs = {
        "elementaryNeighbours": {"numberOfNeighbours": 25, "neighboursMaxDistance": 1, "summitsAccount": n},
        "distElementaryNeighbours": {"numberOfNeighbours": 20, "neighboursMaxDistance": 10, "summitsAccount": n},
        "salesManInRingNeighbours": {"numberOfNeighbours": 10, "neighboursMaxDistance": 1, "summitsAccount": n},
    }
    initPopulation = {
        "elementaryNeighbours": 20,
        "distElementaryNeighbours": 5,
        "salesManInRingNeighbours": 0,
    }

    totalRunTime = 6 # min
    numberOfMigrations = 25



    SolConfig.setWeights(ring_weights, stars_weights)

    subjects = {name: [SolConfig.initialSol() for i in range(initPopulation[name])] for name in kargs}

    InsularCycles = '?'
    lapsCounter = 0
    while time.time()-tic < totalRunTime*60:

        subjects["elementaryNeighbours"] = partialLocalSearch(subjects["elementaryNeighbours"], elementaryNeighbours, kargs["elementaryNeighbours"], msgHeader=f"Lap {lapsCounter+1}/{InsularCycles} - elemN  - ")
        subjects["distElementaryNeighbours"] = partialLocalSearch(subjects["distElementaryNeighbours"], elementaryNeighbours, kargs["distElementaryNeighbours"], msgHeader=f"Lap {lapsCounter+1}/{InsularCycles} - elemN2 - ")
        subjects["salesManInRingNeighbours"] = partialLocalSearch(subjects["salesManInRingNeighbours"], salesManInRingNeighbours, kargs["salesManInRingNeighbours"], msgHeader=f"Lap {lapsCounter+1}/{InsularCycles} - salesM - ")

        subjects = shuffle(subjects, numberOfMigrations=numberOfMigrations)
        lapsCounter += 1

    concatenedSubjects = []
    for key in subjects:
        concatenedSubjects += subjects[key]

    best = min(concatenedSubjects, key=lambda item: item.getCost())

    print(endMsg)

    print(f"Best solution cost: {best.getCost()}")

    toc = time.time()
    sec = time.gmtime(int(toc-tic))
    t = time.strftime("%M min %S sec", sec)
    print(f"Temps d'exécution: {t}")

    best.result(path)
