import random
import matplotlib.pyplot as plt

def init_maze(p,n):
    """
    Returns maze (list of lists of Spots), start column and end column

    maze if of height and width n
    Start is always on the top row
    End is always on the bottom row
    """
    maze=[[Spot(p) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        #make edges
        maze[0][i].is_wall = True;
        maze[n-1][i].is_wall = True;
        maze[i][0].is_wall = True;
        maze[i][n-1].is_wall = True;
    start=random.randint(1, n-2)
    end=random.randint(1, n-2)
    maze[0][start].on_path = True
    maze[0][start].is_dud = True
    maze[n-1][end].is_wall = False

    return maze, start, end


def print_maze(maze):
    for row in maze:
        for spot in row:
            print spot,
        print


class Spot(object):
    def __init__(self, p):
        self.is_wall=(random.random()<p);
        self.is_dud=False; #What does is_dud mean? It's not obvious to me
        self.on_path=False;
    def __repr__(self):
        if self.on_path: return 'o'
        if self.is_wall: return '+'
        else: return ' '
    @property
    def available(self):
        return(all([not self.on_path, not self.is_wall, not self.is_dud]))

def step_solve(maze,loc,path, start, end):
    'Returns True if maze solved, else False'
    n=len(maze)
    x=loc[0];
    y=loc[1];

    # Question: is loc supposed to already be on the path when this function is called?

    if(path[-1] != loc):
        path.append(loc) #because of retracing, it may already be on path
    
    maze[x][y].on_path=True; #to avoid loops

    if y == start and x == 0: #it traced all the way back to start
        return False;
    
    if y == end and x == n-1:
        return True;

    if((maze[x][y].is_dud)):
        return False  #why this second check? We know it's not the start
    
    neighbors = [[x+1, y], [x-1, y], [x, y+1], [x, y-1]]
    for neighbor_x, neighbor_y in neighbors:
        if(maze[neighbor_x][neighbor_y].available):
            solved = step_solve(maze, [neighbor_x, neighbor_y], path, start, end)
            if solved:
                return True

    #all four possibilities have been exhausted, this node is a dud
    maze[x][y].is_dud=True;
    maze[x][y].on_path=False;
     #remove current element
    path.pop(); #remove previous element

    return False

def maze_data(maze_size,numtrials,p):
    num_solved=0

    for _ in range(numtrials):
        maze, start, end = init_maze(p, maze_size)
        path=[[0,start]];
        if (not maze[1][start].is_wall) and step_solve(maze,[1,start],path, start, end): #it solved it
            num_solved+=1
    return float(num_solved)/numtrials

def getandplot(size,numtrials):
    data=[];
    for i in range(0,100,1):
        p=(i+.0)/100
        data.append([size,p,maze_data(size,numtrials,p)])

    
    x,y=[],[]

    for j in range(len(data)):
        x.append(data[j][1])
        y.append(data[j][2])

    plt.plot(x,y,label='size is '+str(size))
    plt.xlabel


def singleton_maze():
    p=.3;
    size=20;
    [maze,start,end]=init_maze(p,size)
    path=[[0,start]];

    print step_solve(maze,[1,start],path, start, end)
    print_maze(maze)

def main():
    n = 20
    getandplot(5,n)
    getandplot(10,n)
    getandplot(15,n)
    getandplot(20,n)
    getandplot(22,n)
 #   plt.legend()
  #  plt.show()
    pass


if __name__ == '__main__':
   main()

   #singleton_maze()
