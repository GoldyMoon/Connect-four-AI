import random
import time
import pygame
import math
import numpy as np
from copy import deepcopy


class connect4Player(object):
	def __init__(self, position, seed=0):
		self.position = position
		self.opponent = None
		self.seed = seed
		random.seed(seed)

	def play(self, env, move):
		move = [-1]

class human(connect4Player):

	def play(self, env, move):
		move[:] = [int(input('Select next move: '))]
		while True:
			if int(move[0]) >= 0 and int(move[0]) <= 6 and env.topPosition[int(move[0])] >= 0:
				break
			move[:] = [int(input('Index invalid. Select next move: '))]

class human2(connect4Player):

	def play(self, env, move):
		done = False
		while(not done):
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()

				if event.type == pygame.MOUSEMOTION:
					pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
					posx = event.pos[0]
					if self.position == 1:
						pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
					else: 
						pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
				pygame.display.update()

				if event.type == pygame.MOUSEBUTTONDOWN:
					posx = event.pos[0]
					col = int(math.floor(posx/SQUARESIZE))
					move[:] = [col]
					done = True

class randomAI(connect4Player):

	def play(self, env, move):
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)
		move[:] = [random.choice(indices)]

class stupidAI(connect4Player):

	def play(self, env, move):
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)
		if 3 in indices:
			move[:] = [3]
		elif 2 in indices:
			move[:] = [2]
		elif 1 in indices:
			move[:] = [1]
		elif 5 in indices:
			move[:] = [5]
		elif 6 in indices:
			move[:] = [6]
		else:
			move[:] = [0]

class minimaxAI(connect4Player):
	
	def eval(self,env,weightboard):
		evalue = 0
		for i in range(0,6):
			for j in range(0,7):
				if(self.position == 2): #Min is the player
					if(env.board[i][j] == 2):
						evalue = evalue + 1 * weightboard[i][j]
					elif(env.board[i][j] == 1):
						evalue = evalue + (-1) * weightboard[i][j]
				elif(self.position == 1): #Max is the player
					if(env.board[i][j] == 1):
						evalue = evalue + 1 * weightboard[i][j]
					elif(env.board[i][j] == 2):
						evalue = evalue + (-1) * weightboard[i][j]
		return evalue

	def simulateMove(self,env,move,player):
		env.board[env.topPosition[move]][move] = player
		env.topPosition[move] -= 1
		env.history[0].append(move)
  
	def MAX(self,env,depth,weightboard):
		if env.gameOver(env.history[0][-1],self.opponent.position):
			return -10000
		if depth == 0:
			return self.eval(env,weightboard)
		score = -10000
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)
		for k in indices:
			child = deepcopy(env)
			self.simulateMove(child,k,self.position)
			chiildscore = self.MIN(child ,depth - 1, weightboard)
			score = max(score,chiildscore)
		return score
   
	def MIN(self,env,depth,weightboard):
			if env.gameOver(env.history[0][-1],self.position):
				return 10000
			if depth == 0:
				return self.eval(env,weightboard)
			score = 10000
			possible = env.topPosition >= 0
			indices = []
			for i, p in enumerate(possible):
				if p: indices.append(i)
			for k in indices:
				child = deepcopy(env)
				self.simulateMove(child,k,self.opponent.position)
				chiildscore = self.MAX(child ,depth - 1, weightboard)
				score = min(score,chiildscore)
			return score
  
	def play(self, env, move):
		weightboard = np.array([[3, 4, 5, 7, 5, 4, 3],
                    [4, 6, 8, 10, 8, 6, 4],
                    [5, 8, 11, 13, 11, 8, 5],
                    [5, 8, 11, 13, 11, 8, 5],
                    [4, 6, 8, 10, 8, 6, 4],
                    [3, 4, 5, 7, 5, 4, 3]])
		env = deepcopy(env)
		env.visualize = False
		depth = 3
		score = -10000
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)
		for k in indices:
			child = deepcopy(env)
			self.simulateMove(child,k,self.position)
			childscore =self.MIN(child,depth - 1,weightboard)
			if childscore > score:
				score = childscore
				move[:] = [k]

class alphaBetaAI(connect4Player):
	def eval(self,env,weightboard):
		evalue = 0
		for i in range(0,6):
			for j in range(0,7):
				if(self.position == 2): #Min is the player
					if(env.board[i][j] == 2):
						evalue = evalue + 1 * weightboard[i][j]
					elif(env.board[i][j] == 1):
						evalue = evalue + (-1) * weightboard[i][j]
				elif(self.position == 1): #Max is the player
					if(env.board[i][j] == 1):
						evalue = evalue + 1 * weightboard[i][j]
					elif(env.board[i][j] == 2):
						evalue = evalue + (-1) * weightboard[i][j]
		return evalue

	def simulateMove(self,env,move,player):
		env.board[env.topPosition[move]][move] = player
		env.topPosition[move] -= 1
		env.history[0].append(move)
  
	def MAX(self,env,depth,weightboard,alpha,beta):
		if env.gameOver(env.history[0][-1],self.opponent.position):
			return -10000
		if depth == 0:
			return self.eval(env,weightboard)
		score = -10000
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)   
		indices.sort(key=lambda i: -weightboard[env.topPosition[i]][i])
		for k in indices:
			child = deepcopy(env)
			self.simulateMove(child,k,self.position)
			chiildscore = self.MIN(child ,depth - 1, weightboard,alpha,beta)
			score = max(score,chiildscore)
			alpha = max(alpha,score)
			if score >= beta:
				break
		return score
   
	def MIN(self,env,depth,weightboard,alpha,beta):
		if env.gameOver(env.history[0][-1],self.position):
			return 10000
		if depth == 0:
			return self.eval(env,weightboard)
		score = 10000
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)
		indices.sort(key=lambda x: weightboard[env.topPosition[x]][x], reverse=True)
		for k in indices:
			child = deepcopy(env)
			self.simulateMove(child,k,self.opponent.position)
			chiildscore = self.MAX(child ,depth - 1, weightboard,alpha,beta)
			score = min(score,chiildscore)
			beta = min(beta,score)
			if score <= alpha:
				break
		return score
  
	def play(self, env, move):
		weightboard = np.array([[3, 4, 5, 7, 5, 4, 3],
                    [4, 6, 8, 10, 8, 6, 4],
                    [5, 8, 11, 13, 11, 8, 5],
                    [5, 8, 11, 13, 11, 8, 5],
                    [4, 6, 8, 10, 8, 6, 4],
                    [3, 4, 5, 7, 5, 4, 3]])
		env = deepcopy(env)
		env.visualize = False
		if(self.position == 1):
			depth = 4
		elif(self.position == 2):
			depth = 5
		alpha = -math.inf
		beta = math.inf
		score = -10000
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)
		for k in indices:
			child = deepcopy(env)
			self.simulateMove(child,k,self.position)
			childscore =self.MIN(child,depth - 1,weightboard,alpha,beta) 
			if childscore > score:
				score = childscore
				move[:] = [k]
    #print("eval score is: ",score)
		#print("done")

SQUARESIZE = 100
BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

ROW_COUNT = 6
COLUMN_COUNT = 7

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)




