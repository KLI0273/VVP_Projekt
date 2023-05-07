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

def dijkstra(inc_mat,maze):
    n,m = np.shape(maze)

    result = np.zeros((2,n*n))
    result[1,:] = np.ones(n*n)*n*n #distance
    result[1,0] = 0
    unvisited = [i for i in range(n*n)]
    connection = []
    for j in range(inc_mat.shape[1]):
        col_slice = inc_mat[:,j]
        idx = [q for q, x in enumerate(col_slice) if x == 1]
        connection.append(idx)
    
    while(unvisited[-1] == n*n-1):

        dst = n*n
        idx = 0
        for i in unvisited:
            if result[1,i] < dst:
                dst = result[1,i]
                idx = i
        g_idx = get_idx(idx,connection)
        dst = result[1,idx] + 1
        for it in g_idx:
            if(dst < result[1,it]): 
                result[0,it] =  idx
                result[1,it] =  dst
        unvisited.remove(idx)

    idx = n*n-1
    path = [idx]
    while(path[-1] != 0):
        idx = int(result[0,idx])
        path.append(idx)

    return path

def get_idx(idx, connection):
    gen = [c for c in connection if c[0] == idx  or c[1] == idx]
    gen = [c[1] if c[0] == idx else c[0] for c in gen]
    return gen

def create_path_matrix(maze, path):
    # Vytvoření matice nul stejného rozměru jako matice s bludištěm
    path_matrix = np.zeros(maze.shape)

    # Projděte cestu a přidejte hrany mezi sousedními uzly
    for i in range(len(path)-1):
        current = path[i]
        next_node = path[i+1]
        path_matrix[current[0], current[1]] = 1
        path_matrix[next_node[0], next_node[1]] = 1

    # Nastavte hodnotu 1 pro průchozí uzly (bunky na cestě), 0 jinak
    path_matrix[maze] = path_matrix[maze].astype(int)

    return path_matrix
