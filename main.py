import copy
import math
import sys
from random import random

STARTBOARD = []
SOLVEDBOARD = [['1', '2', '3', '4'], ['5', '6', '7', '8'], ['9', '10', '11', '12'], ['13', '14', '15', '0']]
BLANK = {}
ORDER = []
MAXDEPTH = 20


def readFromFileToBoard():
    file = open('input.txt', 'r')
    w = file.read(1)  # w - numbers of rows
    file.seek(2)
    k = file.read(1)  # k - numbers of columns
    file.seek(5)  # set postion at the beginning of second line of file
    for line in file:
        STARTBOARD.append(line.split())  # every line is a table with char values
    print(STARTBOARD)


def findZero(board):
    for col in range(0, len(board)):
        for row in range(0, len(board[col])):
            if board[row][col] == '0':
                BLANK['row'] = row
                BLANK['col'] = col
    print(BLANK)


def check(board, solvedBoard):
    if board == solvedBoard:
        return True
    else:
        return False


class Node:
    def __init__(self, board, parent=None, birthMove=None):
        self.board = board
        self.isBoardCorrect = check(self.board, SOLVEDBOARD)
        self.parent = parent
        self.birthMove = birthMove
        self.leftChild = None
        self.rightChild = None
        self.upChild = None
        self.downChild = None
        self.children = []
        self.vistied = False

    def makeChild(self, board, birthMove):
        child = Node(board, self, birthMove)
        self.children.append(child)
        return child

    def move(self, move):
        findZero(self.board)
        y = BLANK['row']
        x = BLANK['col']
        if move == 'L':
            BLANK['col'] = BLANK['col'] - 1
            tempBoard = copy.deepcopy(self.board)
            tempBoard[y][x], tempBoard[y][x - 1] = tempBoard[y][x - 1], tempBoard[y][x]
            # print(tempBoard)
            self.leftChild = self.makeChild(tempBoard, move)
        if move == 'R':
            BLANK['col'] = BLANK['col'] + 1
            tempBoard = copy.deepcopy(self.board)
            tempBoard[y][x], tempBoard[y][x + 1] = tempBoard[y][x + 1], tempBoard[y][x]
            # print(tempBoard)
            self.rightChild = self.makeChild(tempBoard, move)
        if move == 'U':
            BLANK['row'] = BLANK['row'] - 1
            tempBoard = copy.deepcopy(self.board)
            tempBoard[y][x], tempBoard[y - 1][x] = tempBoard[y - 1][x], tempBoard[y][x]
            # print(tempBoard)
            self.upChild = self.makeChild(tempBoard, move)
        if move == 'D':
            BLANK['row'] = BLANK['row'] + 1
            tempBoard = copy.deepcopy(self.board)
            tempBoard[y][x], tempBoard[y + 1][x] = tempBoard[y + 1][x], tempBoard[y][x]
            # print(tempBoard)
            self.downChild = self.makeChild(tempBoard, move)

    def restrictMovement(self, move):
        findZero(self.board)
        y = BLANK['row']
        x = BLANK['col']
        if move == 'L':
            if x == 0:
                return None
            self.move(move)
        if move == 'R':
            if x == 3:
                return None
            self.move(move)
        if move == 'U':
            if y == 0:
                return None  # Ending branch up
            self.move(move)
        if move == 'D':
            if y == 3:
                return None  # Ending branch down
            self.move(move)

    def backMove(self):
        findZero(self.board)
        y = BLANK['row']
        x = BLANK['col']
        if self.birthMove == 'L':
            self.board[y][x], self.board[y][x + 1] = self.board[y][x + 1], self.board[y][x]
        elif self.birthMove == 'R':
            self.board[y][x], self.board[y][x - 1] = self.board[y][x - 1], self.board[y][x]
        elif self.birthMove == 'U':
            self.board[y][x], self.board[y + 1][x] = self.board[y + 1][x], self.board[y][x]
        elif self.birthMove == 'D':
            self.board[y][x], self.board[y - 1][x] = self.board[y - 1][x], self.board[y][x]
        for c in self.children:
            del c
        self.children.clear()
        self.leftChild = None
        self.rightChild = None
        self.upChild = None
        self.downChild = None


def DFS(node, counter=0):
    if node is not None:
        if node.isBoardCorrect is False:
            visited = []
            listOfNodes = []
            visited.append(node)
            listOfNodes.append(node)
            discoveredSolutionFlag = node.isBoardCorrect
            while listOfNodes and discoveredSolutionFlag is False:
                vertex = listOfNodes.pop()
                for o in ORDER:
                    vertex.restrictMovement(o)
                for child in vertex.children:
                    if child.isBoardCorrect is True:
                        print("Wynik:")
                        print(child.board)
                        return child.board
                    if child not in visited:
                        visited.append(child)
                        listOfNodes.append(child)


def BFS(node, counter=0):
    if node is not None:
        visited = []
        listOfNodes = []
        visited.append(node)
        listOfNodes.append(node)
        discoveredSolutionFlag = node.isBoardCorrect
        while listOfNodes and discoveredSolutionFlag is False:
            vertex = listOfNodes.pop(0)
            discoveredSolutionFlag = vertex.isBoardCorrect
            for o in ORDER:
                vertex.restrictMovement(o)
            for child in vertex.children:
                if child.isBoardCorrect is True:
                    print("Wynik:")
                    print(child.board)
                    return child.board
                if child not in visited:
                    visited.append(child)
                    listOfNodes.append(child)


def searchByValue(matrix, value):
    rows = len(matrix)
    columns = len(matrix[0])
    for i in range(0, rows):
        for j in range(0, columns):
            if matrix[i][j] == value:
                return [i, j]


def manhattanDist(matrix, modelMatrix):
    distance = 0
    rows = len(matrix)
    columns = len(matrix[0])
    for i in range(0, rows):
        for j in range(0, columns):
            if matrix[i][j] != modelMatrix[i][j]:
                indexCorrect = searchByValue(modelMatrix, matrix[i][j])
                distance += abs(j - indexCorrect[0]) + abs(i - indexCorrect[1])
    return distance


def hammingDist(matrix, modelMatrix):
    diffCounter = 0
    rows = len(matrix)
    columns = len(matrix[0])
    for i in range(0, rows):
        for j in range(0, columns):
            if matrix[j][i] != modelMatrix[j][i]:
                diffCounter += 1
    return diffCounter


def ASTAR(node, heuristic):
    discoveredSolutionFlag = node.isBoardCorrect
    while discoveredSolutionFlag is False:
        minCost = sys.maxsize
        minCostMove = []
        for o in ORDER:
            node.restrictMovement(o)
        for child in node.children:
            print(child.board)
            if heuristic == 'manhattan':
                cost = manhattanDist(child.board, SOLVEDBOARD)
                if cost < minCost:
                    minCost = cost
                    minCostMove.clear()
                    minCostMove.append(child.birthMove)
            if heuristic == 'hamming':
                cost = hammingDist(child.board, SOLVEDBOARD)
                if cost < minCost:
                    minCost = cost
                    minCostMove.clear()
                    minCostMove.append(child.birthMove)
            child.backMove()
        node.restrictMovement(minCostMove[0])


if __name__ == '__main__':
    readFromFileToBoard()
    findZero(STARTBOARD)
    root = Node(STARTBOARD)
    ORDER = ['L', 'R', 'D', 'U']
    # print(DFS(root))
    ASTAR(root,'hamming')
