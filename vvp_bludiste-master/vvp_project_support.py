import numpy as np
import matplotlib.pylab as plt
import csv
import networkx as nx
import random


#* Nacteni bludiste 
def load_document(string):
    data = open(string, 'r')
    soubor = csv.reader(data, delimiter=',')
    maze = []
    for rows in soubor:
        maze.append([int(cell) for cell in rows])
    data.close()
    return np.array(maze).astype(bool)

#* Vytvoreni matice incidence 
def incidence_matrix(maze):
    n = maze.shape[0]
    rows = n*n
    cols = 2 * rows - n - n
    inc_matrix = np.zeros((rows,cols)) #vytvorima inc matici maximalni mozne velikosti
    edge = 0
    for i in range(n):
        for j in range(n):
            if (maze[i,j] == False): # pokud je bunka pruchozi
                if( i<n-1): # nejme na prave hrane?
                    if(maze[i+1,j] == False): # je bunka na pravo pruchozi?
                        inc_matrix[i * n + j, edge] = 1 #zapis do inc matice (unique index)
                        inc_matrix[(i+1) * n + j, edge] = 1 #zapis do inc matice (unique index)
                        edge += 1
                if( j<n-1): # nejme na spodni hrane?
                    if(maze[i,j+1] == False): # je bunka dole pruchozi?
                        inc_matrix[i * n + j, edge] = 1
                        inc_matrix[i * n + j+1, edge] = 1
                        edge += 1
    inc_matrix = inc_matrix[:,:edge] # orizneme nepouzite sloupce
    return inc_matrix

#* Vykreslení nx grafu
def draw_nx_graph(matrix):
    Graph = nx.Graph()
    n,m = np.shape(matrix)

   # node as true value
   # for i in range(n): 
   #     Graph.add_node(i)
    
    for i in range(m):
        row_matrix = matrix[:,i] # orizneme sloupec
        idx = [i for i, x in enumerate(row_matrix) if x == 1]
        Graph.add_edge(idx[0], idx[1]) # hodnoty kde jsou v i-tem sloupci jednicky zapiseme

    nx.draw(Graph, with_labels=True)
    plt.show()

#* djikstruv algoritmus pro vypocet cesty (nejkratsi)
def dijkstra(inc_mat,maze):
    n,m = np.shape(maze)

    result = np.zeros((2,n*n))
    result[1,:] = np.ones(n*n)*n*n 
    result[1,0] = 0
    unvisited = [i for i in range(n*n)] # vektor vsech nenastivenych bodu
    connection = []
    for j in range(inc_mat.shape[1]):
        col_slice = inc_mat[:,j] # orizneme sloupec
        idx = [q for q, x in enumerate(col_slice) if x == 1] # zjistime ktere bunky jsou propojene
        connection.append(idx)
    
    while(unvisited[-1] == n*n-1): #cyklus co se ukoknci jakmile bude navstivena posledni bunka

        dst = n*n # vzdalenost
        idx = 0
        for i in unvisited: # prochazime vsechny nenastivene uzly
            if result[1,i] < dst: # pokud vzdalenost uzlu od startu je stonks
                dst = result[1,i] # nastaveni stonks vzdalenosti
                idx = i # urceni indexu pro ktery budeme urcovat sousedni bunky
        g_idx = get_idx(idx,connection) # ziskani sousedu
        dst = result[1,idx] + 1 # nastaveni nove vzdalenosti
        for it in g_idx:
            if(dst < result[1,it]): # pokud je vzdalenost stonks
                result[0,it] =  idx # zapiseme do výsledu index z kterého jsme se dostali
                result[1,it] =  dst # zapiseme novou vzdalenost
        unvisited.remove(idx) # odstranime z seznamu neproskoumanych uzlu

    idx = n*n-1 # posledni idx
    path = [idx] # zapiseme posledni idx do cesty
    while(path[-1] != 0): # prochazime dokud nenastavime posledni cast cesty 
        idx = int(result[0,idx]) # nastavime idx na idx dalsi bunky nejkratsi cesty
        path.append(idx) # pridame danou bunku do cesty
        
    path = [[int((i-i%n)/n),int(i%n)] for i in path ] # prevedeni indeksu an x,y/i,j souradnice
    return path

#* pomocná funkce na zjisteni sousedu
def get_idx(idx, connection):
    gen = [c for c in connection if c[0] == idx  or c[1] == idx] # nalezeme bunky s hledanym indexem
    gen = [c[1] if c[0] == idx else c[0] for c in gen] # zapiseme sousedni uzel
    return gen

#* Ziskani matice s nejkratsi cestou
def create_path_matrix(maze, path):
    path_matrix = np.ones(maze.shape)

    for i in range(len(path)-1):
        current = path[i] # aktualni uzel
        next_node = path[i+1] # dalsi uzel
        path_matrix[current[0], current[1]] = 0 #pruchozi uzel v se v matici zapise jako 0
        path_matrix[next_node[0], next_node[1]] = 0

    path_matrix[maze] = path_matrix[maze].astype(int) #pretypujeme

    return path_matrix

#* Generator bludiste
def generator_maze(n, template_number=0):
    maze = np.ones((n,n))
    maze[0,0] = 0 #vynulovani startu
    maze[n-1,n-1] = 0 # vynulovani konce
    indexy = get_template(n, template_number) #upravovatelne indexy

    while True:
        try: #zkousime zda je bludiste pruchozi
            inc = incidence_matrix(maze)
            dijkstra(inc,maze)
            break
        except: # jestli bludiste pruchozi neni tak pridame do bludiste pruchozi bunku z pole
            pos = random.randint(0,len(indexy)-1) #nahodna bunka z pole
            i, j = indexy.pop(pos) # ziskani pozic bunky a odstraneni z listu aby se hodnoty neopakovaly
            maze[i,j] = 0 # nastaveni pruchozi bunky
            #print(len(indexy)) #* pro nedockavce aktualni informace o tom kolik bunek jeste lze odstranit
    return maze.astype(bool)

#* funkce pro zjiskani listu upravovatelnych bunek s mozným vyberem template
def get_template(n, template_number):
    indexy = []

    #Blank
    if(template_number == 0):
        indexy = [(i,j) for i in range(n) for j in range(n)]

    #Slalom diagonal
    if(template_number == 1):
        for i in range(n):
            for j in range(n):
                if (not(i+j in [n+5, n+6] and i>10)) and (not(i+j in [n-5, n-6] and  i<n-10)):
                    if(not(i+j in [n+int(n/1.5), n+int(n/1.5)-1] and j>n*3/4)) and (not(i+j in [n-int(n/1.5), n-int(n/1.5)-1] and  j<n-n*3/4)):
                        indexy.append((i,j))
    #Big Diag
    if(template_number == 2):
        indexy = [(i,j) for i in range(n) for j in range(n) if (not (i+j == n-1)) or i==0 or j==0]
    
    #Slalom horizontal
    if(template_number == 3):
        tretina = int(n/3)
        indexy = [(i,j) for i in range(n) for j in range(n) if not ((i == tretina and j<n*4/5) or (i == 2*tretina and j>n/5))]

    return indexy
