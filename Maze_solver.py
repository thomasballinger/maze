import random
import matplotlib.pyplot as plt

def init_maze(p,n):
	maze=[[Spot(p) for i in range(n)] for j in range(n)]
	for i in range(n):
		#make edges
		maze[0][i].is_wall=True;
		maze[n-1][i].is_wall=True;
		maze[i][0].is_wall=True;
		maze[i][n-1].is_wall=True;
	start=random.randint(1,n-2)
	end=random.randint(1,n-2)
	maze[0][start].is_start=True
	maze[0][start].on_path=True
	maze[0][start].is_dud=True
	maze[n-1][end].is_end=True
	maze[n-1][end].is_wall=False

	return maze, start, end


def print_maze(maze,n):
	for row in maze:
		for col in row:
			print col,
		print


class Spot(object):
	def __init__(self, p):
		self.is_wall=(random.random()<p);
		self.is_dud=False;
		self.on_path=False;
		self.is_start=False; 	
		self.is_end=False;
	def __repr__(self):
		if self.is_start: return 's'
		if self.is_end: return 'e'
		if self.on_path: return 'o'
		if self.is_wall: return '+'
		else: return ' '
	def available(self):
		return(all([not self.on_path,not self.is_wall,not self.is_dud]))


def step_solve(maze,loc,path):
	'zero is returned for success'
	n=len(maze)
	x=loc[0];
	y=loc[1];

	if(path[len(path)-1]!=loc): 
		path.append(loc) #because of retracing, it may already be on path
	
	maze[x][y].on_path=True; #to avoid loops
	if(maze[x][y].is_start): #it traced all the way back to start
		return False;
	
	if maze[x][y].is_end:
		return True;
	if((maze[x][y].is_dud) and (not maze[x][y].is_start)):
		return False
	
	
	
	# try down
	if(maze[x+1][y].available()):
		return step_solve(maze,[x+1,y],path)
	# try up
	if(maze[x-1][y].available()):
		return step_solve(maze,[x-1,y],path)
	#try right
	if(maze[x][y+1].available()):
		return step_solve(maze,[x,y+1], path)
	# try left
	if(maze[x][y-1].available()):
		return step_solve(maze,[x,y-1],path)
	
	#all four possibilities have been exhausted, this node is a dud
	maze[x][y].is_dud=True;
	maze[x][y].on_path=False;
	 #remove current element
	path.pop(); #remove previous element

	return step_solve(maze,path[len(path)-1],path)

def maze_data(maze_size,numtrials,p):
	num_solved=0

	for _ in range(numtrials):
		[maze,start,end]=init_maze(p,maze_size)
		path=[[0,start]];
		if maze[1][start].is_wall:
			pass
		elif step_solve(maze,[1,start],path): #it solved it
			num_solved+=1
	return (num_solved+.0)/numtrials

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

	print step_solve(maze,[1,start],path)
	print_maze(maze,size)	

def main():
	getandplot(5,10000)
	getandplot(10,10000)
	getandplot(15,10000)
	getandplot(20,10000)
	getandplot(22,10000)
	plt.legend()
	plt.show()
	pass


#if __name__ == '__main__':
#	main()
#main()
singleton_maze()