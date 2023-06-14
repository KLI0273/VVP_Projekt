import numpy as np
import matplotlib.pylab as plt
import csv
import networkx as nx
import random
from copy import deepcopy

class Maze:
    def __init__(self, fileName:str = None):
        if(fileName != None):
            self.load(fileName)
            
    def load(self, fileName:str) -> None:
        data = open(fileName, 'r')
        soubor = csv.reader(data, delimiter=',')
        maze = []
        for rows in soubor:
            maze.append([int(cell) for cell in rows])
        data.close()
        self.maze = np.array(maze).astype(bool)

    def incidence_matrix(self) -> None:
        n = self.maze.shape[0]
        rows = n*n
        cols = 2 * rows - n - n
        inc_matrix = np.zeros((rows,cols))
        edge = 0
        for i in range(n):
            for j in range(n):
                if (self.maze[i,j] == False): 
                    if( i<n-1):
                        if(self.maze[i+1,j] == False):
                            inc_matrix[i * n + j, edge] = 1
                            inc_matrix[(i+1) * n + j, edge] = 1
                            edge += 1
                    if( j<n-1):
                        if(self.maze[i,j+1] == False):
                            inc_matrix[i * n + j, edge] = 1
                            inc_matrix[i * n + j+1, edge] = 1
                            edge += 1
        self.inc_matrix = inc_matrix[:,:edge]

    def dijkstra(self) -> None:
        n,m = np.shape(self.maze)

        result = np.zeros((2,n*n))
        result[1,:] = np.ones(n*n)*n*n 
        result[1,0] = 0
        unvisited = [i for i in range(n*n)]
        connection = []
        for j in range(self.inc_matrix.shape[1]):
            col_slice = self.inc_matrix[:,j]
            idx = [q for q, x in enumerate(col_slice) if x == 1]
            connection.append(idx)
        
        while(unvisited[-1] == n*n-1):

            dst = n*n
            idx = 0
            for i in unvisited:
                if result[1,i] < dst:
                    dst = result[1,i]
                    idx = i
            g_idx = Maze.get_idx(idx, connection)
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
            
        self.path = [[int((i-i%n)/n),int(i%n)] for i in path]

    @staticmethod
    def get_idx(idx:int, connection:list[int]) -> int:
        gen = [c for c in connection if c[0] == idx  or c[1] == idx]
        gen = [c[1] if c[0] == idx else c[0] for c in gen]
        return gen
    
    def path_matrix(self) -> None:
        path_matrix = np.ones(self.maze.shape)

        for i in range(len(self.path)): #for i in range(len(self.path)-1):
            current = self.path[i] 
            #next_node = self.path[i+1]
            path_matrix[current[0], current[1]] = 0
            #path_matrix[next_node[0], next_node[1]] = 0

        path_matrix[self.maze] = path_matrix[self.maze].astype(int)
        self.result_matrix = self.maze + path_matrix

    def draw(self) -> None:   
        plt.figure(figsize=(8,4))
        cmap = plt.cm.colors.ListedColormap(['red', 'white', 'black'])
        plt.imshow(self.result_matrix, cmap=cmap)
        plt.show()
    
    def solve(self)->None:
        self.incidence_matrix()
        self.dijkstra()
        self.path_matrix()
    
    def generator_maze(self, n:int, template_number:int = 0) -> None:
        self.maze = np.zeros((n,n))
        indexy = self.get_template(n, template_number)
        pocet_bunek = 1000
        maze_copy = None
        indexy_copy = None
        fail_count = 0
        fail_end = np.ceil(np.sqrt(n))

        while True:
            try:
                if(pocet_bunek >= len(indexy)):
                    pocet_bunek /= 10

                maze_copy = deepcopy(self.maze)
                indexy_copy = deepcopy(indexy)

                for i in range(pocet_bunek):
                    pos = random.randint(0,len(indexy)-1)
                    i, j = indexy.pop(pos)
                    self.maze[i,j] = 1

                self.solve()
                break
            except:
                fail_count += 1
                if(pocet_bunek == 1 and fail_count >= fail_end):
                    break
                if(fail_count >= fail_end): 
                    fail_count = 0
                    pocet_bunek /= 10
                indexy = indexy_copy
                self.maze = maze_copy
           
        self.maze = maze_copy.astype(bool)
    
    def get_template(self, n:int, template_number:int) -> list[tuple[int, int]]:
        indexy = [(i,j) for i in range(n) for j in range(n)]

        #*Blank
        if(template_number == 0):
            pass

        #*Slalom diagonal
        if(template_number == 1):
            for i in range(n):
                for j in range(n):
                    if not((i+j in [n+5, n+6] and i>10) or (i+j in [n-5, n-6] and  i<n-10)):
                        if (i+j in [n+int(n/1.5), n+int(n/1.5)-1] and j>n*3/4) or (i+j in [n-int(n/1.5), n-int(n/1.5)-1] and j<n-n*3/4):
                            self.maze[j,i] = 1
                            indexy.remove((j,i))
                    else:
                        indexy.remove((j,i))
                        self.maze[j,i] = 1

        #*Big Diag
        if(template_number == 2):
            for i in range(n):
                for j in range(n):
                    if not((not (i+j == n-1)) or i==0 or j==0):
                        indexy.remove((i,j))
                        self.maze[i,j] = 1
        
        #*Slalom horizontal
        if(template_number == 3):
            tretina = int(n/3)
            for i in range(n):
                for j in range(n):
                    if(((i == tretina and j<n*4/5) or (i == 2*tretina and j>n/5))):
                        indexy.remove((i,j))
                        self.maze[i,j] = 1

        indexy.remove((0,0))
        indexy.remove((n-1, n-1))

        return indexy

