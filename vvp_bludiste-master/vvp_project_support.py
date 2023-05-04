import numpy as np
import matplotlib.pylab as plt
import csv

def load_document():
    #data = open(f'{string}', 'r')
    data = open('vvp_bludiste-master/data/maze_1.csv', 'r')
    soubor = csv.reader(data, delimiter=',')
    maze = []
    for rows in soubor:
        maze.append([int(cell) for cell in rows])
    data.close
    return np.array(maze).astype(bool)
