import random
import csv
import numpy as np

def bestStars(cout_cycle, cout_horscycle, liste_cycle):
    dictio_etoiles = dict()

    #Déterminer le nombre de sommets dans la matrice
    nb_sommet = len(cout_cycle)

    #Cout total des étoiles
    cout_total_etoiles = 0

    #Liste ensemble des sommets possibles
    liste_ensemble_sommet = list(range(1,nb_sommet+1))

    for sommet in liste_ensemble_sommet:
        if sommet not in liste_cycle:
            minimum = None
            sommet_cycle_minimum = 1
            for etoile in liste_cycle:
                calcul_minimum  = cout_horscycle[sommet-1, etoile-1]
                if minimum is None:
                    minimum = calcul_minimum
                else:
                    if calcul_minimum < minimum:
                        minimum = calcul_minimum
                        sommet_cycle_minimum = etoile

            if (sommet_cycle_minimum not in dictio_etoiles):
                dictio_etoiles[sommet_cycle_minimum] = list()

            dictio_etoiles[sommet_cycle_minimum].append(sommet)

            cout_total_etoiles += minimum

    return dictio_etoiles


class SolConfig:
    ring_weights = None
    stars_weights = None

    def setWeights(ring_weights, stars_weights):
        SolConfig.ring_weights = ring_weights
        SolConfig.stars_weights = stars_weights

    def initialSol():
        N = len(SolConfig.ring_weights)
        newRing = [1]

        for i in range(random.randint(0, N)):
            x = random.randint(2, N)
            if x not in newRing:
                newRing.append(x)
        return SolConfig(newRing)

    def __init__(self, ring):
        self.ring = ring  # list()
        self.stars = bestStars(SolConfig.ring_weights, SolConfig.stars_weights, ring)  # dict() avec key=ring summit et value = list(summits linked to key)
        self.cost = self.computeRingCost() + self.computeStarCost()
        self.datas = ["datas/d1_ring.dat", "datas/d1_star.dat"]

    def getRing(self):
        return self.ring.copy()

    def getStars(self):
        tempDict = dict()
        for key in self.stars:
            tempDict[key] = self.stars[key].copy()
        return tempDict

    def computeRingCost(self):
        ring_cost = 0
        successeur = 1
        for x in reversed(self.ring):
            predecesseur = x
            ring_cost = ring_cost + int(SolConfig.ring_weights[predecesseur-1, successeur-1])
            successeur = x

        return ring_cost

    def computeStarCost(self):
        star_cost = 0
        for x in self.stars:
            tab = self.stars[x]
            for y in tab:
                star_cost = star_cost + int(SolConfig.stars_weights[x-1, y-1])

        return star_cost

    def getCost(self):
        return self.cost

    def toCsv(self):

        for x in self.datas:
            d = x.split(".")
            data_csv = d[0]+".csv"

            with open(x, 'r') as in_file:
                lines = in_file.read().splitlines()
                stripped = [line.replace(",", " ").split() for line in lines]
                grouped = zip(*[stripped]*1)
                with open(data_csv, 'w') as out_file:
                    writer = csv.writer(out_file)
                    for group in grouped:
                        writer.writerows(group)

    def update_csv(self, matrix):
        for x in self.datas:
            np.savetxt(x+"2.csv", matrix, delimiter=",", fmt="%d")

    def result(self, url):
        # sous l'hypothèse que le numéto du jeu se trouvera avant l'extension du fichier
        x = url.split(".")
        num = str(x[1][::-1][0])
        data = "fichiers/Groupe5-Challenge"+num+".txt"
        # resultat = open("fichiers/result.txt", "w")
        resultat = open(data, "w")
        res = "RING "+str(len(self.ring))
        resultat.write(res+"\n")
        for x in self.ring:
            resultat.write(str(x)+" ")

        resultat.write("\n")
        resultat.write("STAR"+"\n")

        for x in self.stars:
            tab = self.stars[x]
            for y in tab:
                resultat.write(str(y)+" "+str(x)+"\n")

        resultat.write("COST "+str(self.cost)+"\n")
        resultat.close()
