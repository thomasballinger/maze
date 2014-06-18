#similar to perc but just needs a path from top row to bottom row
#remember everything is indexed as row column
import random
import matplotlib.pyplot as plt

def init_perc(p,n):
	perc=[[Spot(p) for i in range(n)] for j in range(n)]
	for i in range(n):
		perc[0][i].is_wall=True;
		perc[n-1][i].is_wall=True;
		perc[i][0].is_wall=True;
		perc[i][n-1].is_wall=True;
	return perc

def print_perc(perc):
	for row in perc:
		for col in row:
			print col,
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
	for i in range(1,len(perc)-1):
		if perc[1][i].available():
			reachable.append([1,i])
			perc[1][i].checked=True
	
	if(not reachable):
		return False
	while(reachable):

		#update cur
		cur=reachable.pop()
		x=cur[0];y=cur[1];
		curSpot=perc[x][y]
	
		if x==len(perc)-2:
			break #reached the end

		#add upto four spots to reachable
		#up
		if perc[x][y-1].available():
			reachable[:0]=[[x,y-1]]
			perc[x][y-1].checked=True
		#down
		if perc[x][y+1].available():
			reachable[:0]=[[x,y+1]]
			perc[x][y+1].checked=True
		#left
		if perc[x-1][y].available():
			reachable[:0]=[[x-1,y]]
			perc[x-1][y].checked=True
		#right
		if perc[x+1][y].available():
			if(x+1==len(perc)-2):
				return True
			reachable[:0]=[[x+1,y]]
			perc[x+1][y].checked=True

		

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
	plt.plot(x,y,label='maze size is ' + str(size))


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
	getandplot(100,numtrials)
	getandplot(200,numtrials/5)
	
	plt.ylim([-.1,1.1])
	plt.xlabel('wall density')
	plt.ylabel('proportion of percs that are solvable')
	plt.title('Percolator: Number of trials per point is '+str(numtrials))
	plt.legend()
	plt.show()
	


#if __name__ == '__main__':
#	main()
main()
#singleton_perc()
