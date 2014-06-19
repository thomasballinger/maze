#similar to perc but just needs a path from top row to bottom row
#remember everything is indexed as row column
import random
import matplotlib.pyplot as plt

def init_perc(p,n):
    perc=[[[Spot(p) for i in range(n)] for j in range(n)] for k in range(n)]
    #make walls
    for i in range(n):
        for j in range(n):
            perc[0][i][j].is_wall=True;
            perc[n-1][i][j].is_wall=True;
            perc[i][j][0].is_wall=True;
            perc[i][j][n-1].is_wall=True;
            perc[i][0][j].is_wall=True;
            perc[i][n-1][j].is_wall=True;
    return perc

def print_perc(perc):
    for slab in perc:
        for row in slab:
            for col in row:
                print col,
            print
        print


class Spot(object):
    def __init__(self, p):
        self.is_wall=(random.random()<p);
        self.prev=None;
        self.checked=False;
    def __repr__(self):
        if self.checked: return 'o'
        if self.is_wall: return '+'
        else: return ' '
    def available(self):
        return(all([not self.is_wall,not self.checked]))

def solve_perc(perc):
    reachable=[]
    #top plane is reachable
    for i in range(1,len(perc)-1):
        for j in range(1,len(perc)-1):
            if perc[1][i][j].available():
                reachable.append([1,i,j])
                perc[1][i][j].checked=True
    
    if(not reachable):
        return False
    while(reachable):

        #update cur
        cur=reachable.pop()
        x=cur[0];y=cur[1];z=cur[2];
        curSpot=perc[x][y][z]
    
        if x==len(perc)-2:
            break #reached the end

        #add up to six spots to reachable
        #left
        if perc[x][y-1][z].available():
            reachable[:0]=[[x,y-1,z]]
            perc[x][y-1][z].checked=True
        #right
        if perc[x][y+1][z].available():
            reachable[:0]=[[x,y+1,z]]
            perc[x][y+1][z].checked=True
        #up
        if perc[x-1][y][z].available():
            reachable[:0]=[[x-1,y,z]]
            perc[x-1][y][z].checked=True
        #down
        if perc[x+1][y][z].available():
            if(x+1==len(perc)-2):
                return True
            reachable[:0]=[[x+1,y,z]]
            perc[x+1][y][z].checked=True
        #in
        if perc[x][y][z-1].available():
            reachable[:0]=[[x,y,z-1]]
            perc[x][y][z-1].checked=True
        #out
        if perc[x][y][z+1].available():
            reachable[:0]=[[x,y,z+1]]
            perc[x][y][z+1].checked=True
        

    if(x==len(perc)-2):
        return True

def perc_trials(perc_size,numtrials,p):
    num_solved=0

    for _ in range(numtrials):
        perc=init_perc(p,perc_size)
        if solve_perc(perc): #it solved it
            num_solved+=1
    return (num_solved+.0)/numtrials

def getandplot(size,numtrials):
    data=[];
    for i in range(0,100,1):
        p=(i+.0)/100
        data.append([size,p,perc_trials(size,numtrials,p)])
    x,y=[],[]

    for j in range(len(data)):
        x.append(data[j][1])
        y.append(data[j][2])
    plt.plot(x,y,label='percolator size is ' + str(size))


def singleton_perc():
    p=.3;
    size=60
    perc=init_perc(p,size)
    print solve_perc(perc)
    print_perc(perc)

def main():
    numtrials=100;
    getandplot(20,numtrials)
    getandplot(50,numtrials)
    getandplot(100,numtrials/2)
    getandplot(200,numtrials/5)
    
    plt.ylim([-.1,1.1])
    plt.xlabel('wall density')
    plt.ylabel('proportion of percs that are solvable')
    plt.title('Percolator: Number of trials per point is '+str(numtrials))
    plt.legend()
    plt.show()
    


#if __name__ == '__main__':
#   main()
main()
#singleton_perc()
