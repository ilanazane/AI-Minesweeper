#Some imports
import numpy as np
import matplotlib.pyplot as plt
import random
import queue
import time
from IPython.display import clear_output

#Functions that will be very useful for creating/updating mazes

'''
Define the grid to be working with

**inputs:
dim = dimension size of the grid
n = number of mines

**returns:
board = the grid to be worked with
'''

def environment(dim, n):
    #start with a dim by dim zero array

    board = np.zeros((dim,dim))

    while n > 0:
        i = random.randint(0, dim - 1)
        j = random.randint(0, dim - 1)

        if board[i][j] == 9:
            pass
        else:
            board[i][j] = 9
            n -= 1

    for i in range(0, dim):
        for j in range(0, dim):
            if board[i][j] == 9:
                continue

            #check all the neighbors
            mines = 0
            rightValid = False
            leftValid = False
            upValid = False
            downValid = False
            if j - 1 >= 0:
                leftValid = True
            if j + 1 < len(board):
                rightValid = True
            if i + 1 < len(board):
                downValid = True
            if i - 1 >= 0:
                upValid = True

            #check left
            if leftValid == True:
                #check left adjacent
                if board[i][j-1] == 9:
                    #mine is here
                    mines += 1
                else:
                    #no mine is here
                    pass
                #check left & up
                if upValid == True:
                    if board[i-1][j-1] == 9:
                        #mine is here
                        mines += 1
                    else:
                        #no mine is here
                        pass
                #check left & down
                if downValid == True:
                    if board[i+1][j-1] == 9:
                        #mine is here
                        mines += 1
                    else:
                        #no mine is here
                        pass

            #check right
            if rightValid == True:
                #check right adjacent
                if board[i][j+1] == 9:
                    #mine is here
                    mines += 1
                else:
                    #no mine is here
                    pass
                #check right & up
                if upValid == True:
                    if board[i-1][j+1] == 9:
                        #mine is here
                        mines += 1
                    else:
                        #no mine is here
                        pass
                #check right & down
                if downValid == True:
                    if board[i+1][j+1] == 9:
                        #mine is here
                        mines += 1
                    else:
                        #no mine is here
                        pass

            #check up adjacent
            if upValid == True:
                if board[i-1][j] == 9:
                    #mine is here
                    mines += 1
                else:
                    #no mine is here
                    pass

            #check down adjacent
            if downValid == True:
                if board[i+1][j] == 9:
                    #mine is here
                    mines += 1
                else:
                    #no mine is here
                    pass

            board[i][j] = mines

    return board

'''
A Method to Check the Neighbors of a Cell

**inputs:
possible_moves = array of coordinates for the remaining moves
coord = tuple containing the coordinates

**returns:
neighbors = the list of neighbors for the given coordinate
'''

def checkNeighbors(possible_moves, coord):
    neighbors = []
    i = coord[0]
    j = coord[1]

    if (i+1, j) in possible_moves:
        neighbors.append((i+1, j))

    if (i-1, j) in possible_moves:
        neighbors.append((i-1, j))

    if (i, j+1) in possible_moves:
        neighbors.append((i, j+1))

    if (i, j-1) in possible_moves:
        neighbors.append((i, j-1))

    if (i+1, j+1) in possible_moves:
        neighbors.append((i+1, j+1))

    if (i-1, j-1) in possible_moves:
        neighbors.append((i-1, j-1))

    if (i+1, j-1) in possible_moves:
        neighbors.append((i+1, j-1))

    if (i-1, j+1) in possible_moves:
        neighbors.append((i-1, j+1))

    return neighbors

'''
A Method to Update the Agent Board

**inputs:
coord = tuple containing the coordinates
main_board = the main board
agent_board = the agent board

**returns:
agent_board = the grid to be worked with
coord = tuple containing the coordinates
clue = number of adjacent mines
'''

def updateBoard(coord, main_board, agent_board):
    i = coord[0]
    j = coord[1]
    agent_board[i][j] = main_board[i][j]
    clue = agent_board[i][j]
    return agent_board, coord, clue

'''
A Method to Check the Number of Uncovered Mines for a Cell

**inputs:
board = the agent board
coord = tuple containing the coordinates

**returns:
mines = the number of neighboring mines
'''

def checkMines(board, coord):
    #check all the neighbors
    mines = 0
    i = coord[0]
    j = coord[1]
    rightValid = False
    leftValid = False
    upValid = False
    downValid = False
    if j - 1 >= 0:
        leftValid = True
    if j + 1 < len(board):
         rightValid = True
    if i + 1 < len(board):
         downValid = True
    if i - 1 >= 0:
        upValid = True

    #check left
    if leftValid == True:
        #check left adjacent
        if int(board[i][j-1]) == 9 or board[i][j-1] == 0.5:
            #mine is here
            mines += 1
        else:
            #no mine is here
            pass
        #check left & up
        if upValid == True:
            if int(board[i-1][j-1]) == 9 or board[i-1][j-1] == 0.5:
                #mine is here
                mines += 1
            else:
                #no mine is here
                pass
        #check left & down
        if downValid == True:
            if int(board[i+1][j-1]) == 9 or board[i+1][j-1] == 0.5:
                #mine is here
                mines += 1
            else:
                #no mine is here
                pass

    #check right
    if rightValid == True:
        #check right adjacent
        if int(board[i][j+1]) == 9 or board[i][j+1] == 0.5:
            #mine is here
            mines += 1
        else:
            #no mine is here
            pass
        #check right & up
        if upValid == True:
            if int(board[i-1][j+1]) == 9 or board[i-1][j+1] == 0.5:
                 #mine is here
                mines += 1
            else:
                #no mine is here
                pass
        #check right & down
        if downValid == True:
            if int(board[i+1][j+1]) == 9 or board[i+1][j+1] == 0.5:
                #mine is here
                mines += 1
            else:
                #no mine is here
                pass

    #check up adjacent
    if upValid == True:
        if int(board[i-1][j]) == 9 or board[i-1][j] == 0.5:
            #mine is here
            mines += 1
        else:
            #no mine is here
            pass

    #check down adjacent
    if downValid == True:
        if int(board[i+1][j]) == 9 or board[i+1][j] == 0.5:
            #mine is here
            mines += 1
        else:
            #no mine is here
            pass

    return mines

'''
Initialize blank equation to be used for inference

**inputs:
dim = the dimension size

**returns:
equation = a list of dim**2 zeros
'''

def equation(dim):
    equation = []
    while len(equation) < dim*dim:
        equation.append(0)
    return equation
