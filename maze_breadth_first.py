import random
import matplotlib.pyplot as plt

def init_maze(p,n):
    """
    Returns maze (a list of lists of spots), start column, end column

    start is always in the top row
    end is always in the bottom row
    """
    maze=[[Spot(p) for i in range(n)] for j in range(n)]
    for i in range(n):
        #make edges
        maze[0][i].is_wall=True;
        maze[n-1][i].is_wall=True;
        maze[i][0].is_wall=True;
        maze[i][n-1].is_wall=True;
    start=random.randint(1,n-3)
    end=random.randint(1,n-3)
    maze[0][start].is_start=True
    maze[0][start].on_path=True
    maze[0][start].is_wall=True
    maze[n-1][end].is_end=True
    maze[n-1][end].is_wall=False
    #clear a little window
    maze[1][start].is_wall=False
    maze[1][start+1].is_wall=False
    maze[1][start-1].is_wall=False
    maze[n-2][end].is_wall=False
    maze[n-2][end+1].is_wall=False
    maze[n-2][end-1].is_wall=False


    return maze, start, end


def print_maze(maze):
    for row in maze:
        for col in row:
            print col,
        print


class Spot(object):
    def __init__(self, p):
        self.is_wall=(random.random()<p);
        self.prev=None;
        self.is_start=False;    
        self.is_end=False;
        self.checked=False;
    def __repr__(self):
        if self.is_start: return 's'
        if self.is_end: return 'e'
        if self.checked: return 'o'
        if self.is_wall: return '+'
        else: return ' '
    def available(self):
        return(all([not self.is_wall,not self.checked]))

def solve_maze(maze,start):
    reachable=[[1,start]] #list of reachable spots
    curSpot=maze[1][start]
    if curSpot.is_wall:
        return False
    curSpot.checked=True;

    while(reachable):
        
        #update cur
        cur=reachable.pop()
        x=cur[0];y=cur[1];
        curSpot=maze[x][y]
            

        if curSpot.is_end:
            break

        #add upto four spots to reachable
        #up
        if maze[x][y-1].available():
            reachable[:0]=[[x,y-1]]
            maze[x][y-1].checked=True
        #down
        if maze[x][y+1].available():
            reachable[:0]=[[x,y+1]]
            maze[x][y+1].checked=True
        #left
        if maze[x-1][y].available():
            reachable[:0]=[[x-1,y]]
            maze[x-1][y].checked=True
        #right
        if maze[x+1][y].available():
            reachable[:0]=[[x+1,y]]
            maze[x+1][y].checked=True

        

    if(curSpot.is_end):
        return True
    else: 
        return False    


def maze_trials(maze_size,numtrials,p):
    num_solved=0

    for _ in range(numtrials):
        [maze,start,end]=init_maze(p,maze_size)
        path=[[0,start]];
        if maze[1][start].is_wall:
            pass
        elif solve_maze(maze,start): #it solved it
            num_solved+=1
    return (num_solved+.0)/numtrials

def getandplot(size,numtrials):
    data=[];
    for i in range(0,100,1):
        p=(i+.0)/100
        data.append([size,p,maze_trials(size,numtrials,p)])

    
    x,y=[],[]

    for j in range(len(data)):
        x.append(data[j][1])
        y.append(data[j][2])

    plt.plot(x,y,label='maze size is '+str(size))
    


def singleton_maze():
    p=.4;
    size=20;
    [maze,start,end]=init_maze(p,size)
        
    print solve_maze(maze,start)
    print_maze(maze)

def main():
    #getandplot(10,200)
    #print "10"
    #getandplot(20,200)
    #print "20"
    #getandplot(30,200)
    numtrials=20;
    getandplot(60,numtrials)
    #getandplot(70,150)
    #print "30"
    
    plt.xlabel('probability of wall')
    plt.ylabel('proportion of mazes that are solvable')
    plt.title('Numter of trials per point is '+str(numtrials))
    plt.legend()
    plt.show()
    


#if __name__ == '__main__':
#   main()
#singleton_maze()
#main()
