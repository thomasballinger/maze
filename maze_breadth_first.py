import random
import matplotlib.pyplot as plt


class Maze(object):
    def __init__(self, p, n):
        """
        Returns maze (a list of lists of spots), start column, end column

        start is always in the top row
        end is always in the bottom row
        """
        self.n = n
        self.board=[[Spot(p) for i in range(n)] for j in range(n)]

        self.start=random.randint(1,n-3)
        self.board[0][self.start].is_start=True
        self.board[0][self.start].is_wall=True

        self.end=random.randint(1,n-3)
        self.board[n-1][self.end].is_end=True
        self.board[n-1][self.end].is_wall=False

        self.make_edges()
        self.clear_windows()

    def make_edges(self):
        for i in range(self.n):
            #make edges
            self.board[0][i].is_wall=True;
            self.board[self.n-1][i].is_wall=True;
            self.board[i][0].is_wall=True;
            self.board[i][self.n-1].is_wall=True;

    def clear_windows(self):
        """Makes maze not impossible one first and last moves

        the three spaces within the maze proper (excluding the
        outer wall) are made not walls
        """
        for spot in (self.board[1][self.start-1:self.start+1]
                     + self.board[self.n-2][self.end-1:self.end+1]):
            spot.is_wall = False

    def __str__(self):
        return '\n'.join(' '.join(str(spot) for spot in row) for row in self.board)

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
        if self.is_wall: return u'\u25d9'.encode('utf8')
        else: return ' '
    def available(self):
        return(all([not self.is_wall,not self.checked]))

def neighbors(x, y):
    return [[x, y-1], [x, y+1], [x-1, y], [x+1, y]]

def solve_maze(maze,start):

    reachable = []

    def visit(row, column):
        reachable.insert(0, [row, column])
        maze[row][column].checked = True

    visit(1, start)
    curSpot=maze[1][start]
    assert not curSpot.is_wall

    while(reachable):

        #update cur
        x, y = reachable.pop()
        curSpot=maze[x][y]

        if curSpot.is_end:
            return True

        #add upto four spots to reachable
        for neighbor_x, neighbor_y in neighbors(x, y):
            if maze[neighbor_x][neighbor_y].available():
                visit(neighbor_x, neighbor_y)

    return False


def maze_trials(maze_size,numtrials,p):
    num_solved=0

    for _ in range(numtrials):
        maze = Maze(p, maze_size)
        path = [[0, maze.start]];
        if solve_maze(maze.board, maze.start): #it solved it
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
    maze = Maze(p, size)

    print solve_maze(maze.board, maze.start)
    print maze

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
#main()
singleton_maze()
