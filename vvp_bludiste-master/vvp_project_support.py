import numpy as np
import matplotlib.pylab as plt
import csv

def load_document(string):
    data = open(string, 'r')
    soubor = csv.reader(data, delimiter=',')
    maze = []
    for rows in soubor:
        maze.append([int(cell) for cell in rows])
    data.close()
    return np.array(maze).astype(bool)


