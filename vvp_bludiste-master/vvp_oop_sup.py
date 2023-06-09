import numpy as np
import matplotlib.pylab as plt
import csv
import networkx as nx
import random

class Maze:
    def __init__(self, fileName:str = None):
        if(fileName is not None):
            self.load(fileName)
            
    def load(self, fileName:str) -> None:
        '''
        Vstup:
            filename - cesta k souboru s bludištěm
        Výstup:
            nic (vytvoří self.maze)
        '''
        data = open(fileName, 'r')
        soubor = csv.reader(data, delimiter=',')
        maze = []
        for rows in soubor:
            maze.append([int(cell) for cell in rows])
        data.close()
        self.maze = np.array(maze).astype(bool)

    def incidence_matrix(self) -> None:
        '''
        Vstup:
            nic (vyžaduje maze vygenerovaný pomocí "maze.generator_maze" nebo načtený z souboru pomocí "maze.load")
        Výstup:
            nic (vytvoří self.inc_matrix)
        '''
        n = self.maze.shape[0]
        rows = n*n
        cols = 2 * rows - n - n
        inc_matrix = np.zeros((rows,cols))
        edge = 0
        for i in range(n):
            for j in range(n):
                if (self.maze[i,j] == False): 
                    if( i<n-1):
                        if(not self.maze[i+1,j]):
                            inc_matrix[i * n + j, edge] = 1
                            inc_matrix[(i+1) * n + j, edge] = 1
                            edge += 1
                    if( j<n-1):
                        if(not self.maze[i,j+1]):
                            inc_matrix[i * n + j, edge] = 1
                            inc_matrix[i * n + j+1, edge] = 1
                            edge += 1
        self.inc_matrix = inc_matrix[:,:edge]

    def dijkstra(self) -> None:
        '''
        Vstup:
            nic (vyžaduje inc_matrix vygenerovaný pomocí "maze.incidence_matrix")
        Výstup:
            nic (vytvoří self.path)
        ''' 
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
            g_idx = get_idx(idx, connection)
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

    def path_matrix(self) -> None:
        '''
        Vstup:
            nic (vyžaduje path vygenerovaný pomocí "maze.dijkstra")
        Výstup:
            nic (vytvoří self.result_matrix)
        ''' 
        path_matrix = np.ones(self.maze.shape)

        for i in range(len(self.path)): #for i in range(len(self.path)-1):
            current = self.path[i] 
            #next_node = self.path[i+1]
            path_matrix[current[0], current[1]] = 0
            #path_matrix[next_node[0], next_node[1]] = 0

        path_matrix[self.maze] = path_matrix[self.maze].astype(int)
        self.result_matrix = self.maze + path_matrix

    def draw(self) -> None:
        '''
        Vstup:
            nic (vyžaduje result_matrix načtenou pomocí "maze.solve" nebo "maze.path_matrix")
        Výstup:
            vykreslí bludiště (nevrací nic)
        '''  
        plt.figure(figsize=(8,4))
        cmap = plt.cm.colors.ListedColormap(['red', 'white', 'black'])
        plt.imshow(self.result_matrix, cmap=cmap)
        plt.show()
    
    def solve(self)->None:
        '''
        Vstup:
            nic (vyžaduje načtené bludiště z souboru pomocí "maze.load" nebo vygenerované pomocí "maze.generator_maze")
        Výstup:
            Pro bludiště načtené v self.maze 
            1) vytvoří matici incidence
            2) najde nejkratší cestu pomocí djikstrova algoritmu
            3) vytovří result_matrix kterou lze zobrazit pomocí "maze.draw"
        '''
        self.incidence_matrix()
        self.dijkstra()
        self.path_matrix()
    
    def generator_maze(self, n:int, template_number:int = 0) -> None:
        '''
        Vstup:
            n - rozměr bludiště
            template_number - výběr přednastavených šablon
        Výstup:
            Přímo nevrací nic (do proměnné "self.maze" uloží bludiště)
        '''
        self.maze = np.zeros((n,n)).astype(bool)
        indexy = self.get_template(n, template_number)
        pocet_bunek = 1000
        indexy_used = []
        fail_count = 0
        fail_end = n#int(np.ceil(np.sqrt(n)))

        while True:
            
            try:
                if(pocet_bunek >= len(indexy)):
                    pocet_bunek = int(pocet_bunek/10)
                    continue

                for _ in range(pocet_bunek):
                    pos = random.randint(0,len(indexy)-1)
                    i, j = indexy.pop(pos)
                    self.maze[i,j] = True
                    indexy_used.append((i,j))
                self.solve()
                indexy_used.clear()
                
            except:
                for idx in indexy_used:
                    self.maze[idx[0], idx[1]] = False
                indexy.extend(indexy_used)
                indexy_used.clear()

                fail_count += 1
                if(pocet_bunek == 1 and fail_count >= fail_end):
                    break
                if(fail_count >= fail_end): 
                    fail_count = 0
                    pocet_bunek = int(pocet_bunek/10)

        self.maze = self.maze.astype(bool)
    
    def get_template(self, n:int, template_number:int) -> list[tuple[int, int]]:
        '''
        Vstup:
            n - rozměr bludiště
            template_number - výběr přednastavených šablon
        Výstup:
            List opsahující tuply s dvěmi int hodnoty "list[tuple[int, int]]" obsahující souřadnice i a j v bludiši na které se budou doplňovat stěny
        '''

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

def get_idx(idx:int, connection:list[int]) -> int:
        '''
        Vstup:
            idx - uzel pro kterého hledáme sousedy
            connection - list všech sousedů v komponentě obsahující uzel idx
        Výstup:
            sousedy uzlu idx
        '''
        gen = [c for c in connection if c[0] == idx  or c[1] == idx]
        gen = [c[1] if c[0] == idx else c[0] for c in gen]
        return gen