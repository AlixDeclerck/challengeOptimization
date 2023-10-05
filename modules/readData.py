import numpy as np
import sys

def readData(path):
    np.set_printoptions(threshold=sys.maxsize) #permet d'afficher la totalité de la matrice

    with open(path) as f:
        N=int(f.readline().rstrip("\n"))  #nombre de sommets

        costs_in=np.empty((0,N), int) #tableau contenant la matrice des coûts si le sommet est dans le ring
        costs_out=np.empty((0,N), int) #tableau contenant la matrice des coûts si le sommet n'est pas dans le ring
        i=0 #numéros de ligne

        for lines in f.readlines():
            i+=1
            line=lines.split()

            if i<=N :
                costs_in = np.vstack ((costs_in, np.array(line)) )
                costs_in = costs_in.astype(np.int)

            else :
                costs_out = np.vstack ((costs_out, np.array(line)) )
                costs_out = costs_out.astype(np.int)

    return (costs_in, costs_out, N)


if __name__ == '__main__':
    path = './fichiers/data1.dat'
    readData(path)
