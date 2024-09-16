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
import random

class MyAI(AI):
    def __init__(self, rowDimension, colDimension, totalMines, startX, startY):
        self.rowDimension = rowDimension
        self.colDimension = colDimension
        self.totalMines = totalMines
        self.startX = startX
        self.startY = startY

        self.board = []
        for _ in range(rowDimension):
            row = []
            for _ in range(colDimension):
                row.append(-1)
            self.board.append(row)

        self.cellsToUncover = [(startX, startY)]
        self.flaggedCells = set()
        self.safeCellsToUncover = set()
        self.processedCells = set()
        self.minesInfo = {}


    def getAction(self, numAdjacentMines: int):
        if self.cellsToUncover:
            currentX, currentY = self.cellsToUncover.pop(0)
            self.board[currentX][currentY] = numAdjacentMines
            self.processedCells.add((currentX, currentY))
            self.updateMinesInfo(currentX, currentY, numAdjacentMines)

        self.getSafeAndFlags()

        if self.safeCellsToUncover:
            nextX, nextY = self.safeCellsToUncover.pop()
            if (nextX, nextY) not in self.processedCells:
                self.cellsToUncover.append((nextX, nextY))
                return Action(AI.Action.UNCOVER, nextX, nextY)

        for cell in self.flaggedCells:
            if self.board[cell[0]][cell[1]] != 9:
                self.board[cell[0]][cell[1]] = 9
                return Action(AI.Action.FLAG, cell[0], cell[1])

        nextMove = self.getBestMove()
        if nextMove:
            self.cellsToUncover.append(nextMove)
            return Action(AI.Action.UNCOVER, nextMove[0], nextMove[1])

        return Action(AI.Action.LEAVE)


    def updateMinesInfo(self, x, y, numAdjacentMines):
        self.minesInfo[(x, y)] = numAdjacentMines

        if numAdjacentMines == 0:
            for deltaX, deltaY in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
                neighborX, neighborY = x + deltaX, y + deltaY
                if 0 <= neighborX < self.rowDimension and 0 <= neighborY < self.colDimension and self.board[neighborX][neighborY] == -1:
                    self.safeCellsToUncover.add((neighborX, neighborY))


    def getSafeAndFlags(self):
        for x in range(self.rowDimension):
            for y in range(self.colDimension):
                numAdjacentMines = self.board[x][y]
                if numAdjacentMines not in [-1, 9, 0]:
                    coveredCells, flaggedCells = self.getCoveredAndFlagged(x, y)
                    if flaggedCells == numAdjacentMines and coveredCells:
                        for coveredX, coveredY in coveredCells:
                            self.safeCellsToUncover.add((coveredX, coveredY))
                    elif flaggedCells + len(coveredCells) == numAdjacentMines:
                        for coveredX, coveredY in coveredCells:
                            self.flaggedCells.add((coveredX, coveredY))


    def getCoveredAndFlagged(self, x, y):
        coveredCells = []
        flaggedCells = 0
        for deltaX, deltaY in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            neighborX, neighborY = x + deltaX, y + deltaY
            if 0 <= neighborX < self.rowDimension and 0 <= neighborY < self.colDimension:
                if self.board[neighborX][neighborY] == -1:
                    coveredCells.append((neighborX, neighborY))
                elif (neighborX, neighborY) in self.flaggedCells:
                    flaggedCells += 1
        return coveredCells, flaggedCells


    def getBestMove(self):
        minProb = float('inf')
        bestMove = None
        for x in range(self.rowDimension):
            for y in range(self.colDimension):
                if self.board[x][y] == -1:
                    prob = self.getMineProb(x, y)
                    if prob < minProb:
                        minProb = prob
                        bestMove = (x, y)
        return bestMove


    def getMineProb(self, x, y):
        prob = 0
        weightSum = 0
        for deltaX, deltaY in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            neighborX, neighborY = x + deltaX, y + deltaY
            if 0 <= neighborX < self.rowDimension and 0 <= neighborY < self.colDimension:
                if (neighborX, neighborY) in self.minesInfo:
                    numAdjacentMines = self.minesInfo[(neighborX, neighborY)]
                    coveredCells, flaggedCells = self.getCoveredAndFlagged(neighborX, neighborY)
                    if coveredCells:
                        distanceWeight = 1 / (abs(x - neighborX) + abs(y - neighborY))
                        prob += (numAdjacentMines - flaggedCells) / len(coveredCells) * distanceWeight
                        weightSum += distanceWeight
        if weightSum == 0:
            return float('inf')
        return prob / weightSum
