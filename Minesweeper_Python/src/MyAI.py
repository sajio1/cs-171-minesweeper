# ==============================CS-199==================================
# FILE:			MyAI.py
#
# AUTHOR: 		Justin Chung
#
# DESCRIPTION:	This file contains the MyAI class. You will implement your
#				agent in this file. You will write the 'getAction' function,
#				the constructor, and any additional helper functions.
#
# NOTES: 		- MyAI inherits from the abstract AI class in AI.py.
#
#				- DO NOT MAKE CHANGES TO THIS FILE.
# ==============================CS-199==================================

from AI import AI
from Action import Action


class MyAI( AI ):

	def __init__(self, rowDimension, colDimension, totalMines, startX, startY):

		########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################
		# initialize the AI's knowledge space
		self.rowDimension = rowDimension
		self.colDimension = colDimension
		self.totalMines = totalMines
		self.startX = startX
		self.startY = startY

		# keep tracking uncover cells and their corresponding numbers
		self.board = [[-1 for _ in range(colDimension)] for _ in range(rowDimension)]
		self.board[startX][startY] = 0

		# Track cells to uncover or flag
		self.uncoverQueue = [(startX, startY)]
		self.flagged = set()
		self.safeToUncover = set()
		self.movesMade = set()
		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################

		
	def getAction(self, number: int) -> "Action Object":

		########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################
		# Update the board with the given number for the last uncovered cell
		if self.uncoverQueue:
			x, y = self.uncoverQueue.pop(0)
			self.board[x][y] = number
			self.movesMade.add((x, y))

			if number == 0:
				for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
					nx, ny = x + dx, y + dy
					if 0 <= nx < self.rowDimension and 0 <= ny < self.colDimension and self.board[nx][ny] == -1:
						self.safeToUncover.add((nx, ny))

		if self.safeToUncover:
			x, y = self.safeToUncover.pop()
			if (x, y) not in self.movesMade:
				self.uncoverQueue.append((x, y))
				return Action(AI.Action.UNCOVER, x, y)

		# Flag the mine 
		for i in range(self.rowDimension):
			for j in range(self.colDimension):
				if self.board[i][j] == -1 and self.totalMines == 1 and (i, j) not in self.flagged:
					self.flagged.add((i, j))
					return Action(AI.Action.FLAG, i, j)

		# If no certain moves, random guess
		for i in range(self.rowDimension):
			for j in range(self.colDimension):
				if self.board[i][j] == -1 and (i, j) not in self.flagged and (i, j) not in self.movesMade:
					self.uncoverQueue.append((i, j))
					return Action(AI.Action.UNCOVER, i, j)

		return Action(AI.Action.LEAVE)
		# uncover the next cell in the queue
		if self.uncoverQueue:
			x, y = self.uncoverQueue.pop(0)
			return Action(AI.Action.UNCOVER, x, y)

		
		return Action(AI.Action.LEAVE)
		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################
