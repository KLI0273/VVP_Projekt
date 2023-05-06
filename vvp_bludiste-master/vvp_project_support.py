import numpy as np
import matplotlib.pylab as plt
import csv
from scipy.sparse import csr_matrix
from scipy.sparse import lil_matrix
import networkx as nx
import scipy.sparse as sparse


#* Nacteni bludiste 
def load_document(string):
    data = open(string, 'r')
    soubor = csv.reader(data, delimiter=',')
    maze = []
    for rows in soubor:
        maze.append([int(cell) for cell in rows])
    data.close()
    return np.array(maze).astype(bool)

def incidence_matrix(maze):
    n = maze.shape[0]
    rows = n*n
    cols = 2 * rows - n - n
    inc_matrix = np.zeros((rows,cols))
    edge = 0
    for i in range(n):
        for j in range(n):
            if (maze[i,j] == False):
                if( i<n-1):
                    if(maze[i+1,j] == False):
                        inc_matrix[i * n + j, edge] = 1
                        inc_matrix[(i+1) * n + j, edge] = 1
                        edge += 1
                if( j<n-1):
                    if(maze[i,j+1] == False):
                        inc_matrix[i * n + j, edge] = 1
                        inc_matrix[i * n + j+1, edge] = 1
                        edge += 1
    inc_matrix = inc_matrix[:,:edge]
    return inc_matrix

def draw_nx_graph(matrix):
    Graph = nx.Graph()
    n,m = np.shape(matrix)

#    for i in range(n): 
#        Graph.add_node(i)
    
    for i in range(m):
        row_matrix = matrix[:,i]
        idx = [i for i, x in enumerate(row_matrix) if x == 1]
        Graph.add_edge(idx[0], idx[1])

    nx.draw(Graph, with_labels=True)
    plt.show()
