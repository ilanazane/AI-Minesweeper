from MinesweeperMethods import *
from MinesweeperVisuals import game

'''
The Actual Game to be Played by our Agent

***********************NO INFERENCE****************************

**inputs:
dim = dimension size of the grid
n = number of mines

**returns:

'''

def BasicMinesweeper(dim, n):

    #create our main board and the board the agent will see
    main_board = environment(dim, n)
    agent_board = environment(dim, 0) + 11

    #our three fringes, which make up our general knowledge base
    mineFringe = []
    safeFringe = []
    KB = []

    #a list of the moves made in order to be used in pygame
    moveOrder = []

    #populate a list of all the possible moves we can make, which will keep track of moves that can be made
    possible_moves = []
    for i in range(0, dim):
        for j in range(0, dim):
            possible_moves.append((i, j))


    #play until we finish the game
    gameFinished = False
    while gameFinished == False:

        #our terminating condition
        if len(possible_moves)==0:
            gameFinished=True

            clear_output()


            #UNCOMMENT TO SHOW BOARD OUTPUTS
            '''
            print("Agent's Board:")
            print(agent_board)
            print("The Actual Board:")
            print(main_board)
            '''

            #check our final score (# of correctly identified mines/# of total mines)
            total, correct = 0, 0
            for i in range(0, dim):
                for j in range(0, dim):
                    if main_board[i][j] == 9:
                        total += 1
                    if agent_board[i][j] == 0.5:
                        correct += 1

            #run our visuals via pygame
            game(len(main_board), main_board, environment(dim, 0) + 11, moveOrder)

            score = correct/total
            print(score)
            return score

        else:

            '''
            #CHECK THE MINE FRINGE
            '''

            #if nothing in the mine fringe pass to next step
            if len(mineFringe) == 0:
                pass

            #immediately flag things in mine fringe
            else:

                #go through the mineFringe and flag spots until the fringe is empty again
                while len(mineFringe) != 0:

                    #if the move has already been made, remove from minefringe
                    if not(mineFringe[0] in possible_moves):
                        mineFringe.remove(mineFringe[0])
                        continue

                    #flag a spot with 0.5
                    agent_board[mineFringe[0][0]][mineFringe[0][1]] = 0.5

                    #remove from possible moves and mine fringe
                    possible_moves.remove(mineFringe[0])
                    moveOrder.append((mineFringe[0], 0.5))
                    mineFringe.remove(mineFringe[0])

                #restarts main while loop from beginning
                continue

            '''
            #CHECK THE SAFE FRINGE
            '''

            #if nothing in the safe fringe pass to next step
            if len(safeFringe) == 0:
                pass

            #immediately open things in safe fringe
            else:

                #go through the safeFringe and open spots until the fringe is empty again
                while len(safeFringe) != 0:

                    #if the move has already been made
                    if not(safeFringe[0] in possible_moves):
                        safeFringe.remove(safeFringe[0])
                        continue

                    i = safeFringe[0][0]
                    j = safeFringe[0][1]

                    #open a spot if it is in the safe fringe
                    agent_board, coord, clue = updateBoard((i,j), main_board, agent_board)

                    #add move to KB, then remove from possible moves and mine fringe
                    KB.append([coord, clue, len(checkNeighbors(possible_moves, coord)), clue])
                    possible_moves.remove(safeFringe[0])
                    moveOrder.append((safeFringe[0], clue))
                    safeFringe.remove(safeFringe[0])

                #restarts main while loop from beginning
                continue

            '''
            #CHECK THE KNOWLEDGE BASE
            '''
            #the knowledge base if of the form [(i,j), tempClue, numNeighbors, clue]

            #if nothing in the KB pass to next step
            if len(KB) == 0:
                pass

            #look through our KB for moves to add to safe fringe or mine fringe
            else:
                #make a list for things to be removed from KB
                for item in range(0, len(KB)):

                    #updates the value of adjacent neighbors in the KB
                    KB[item][2] = len(checkNeighbors(possible_moves, KB[item][0]))

                    #Update the temporary clue
                    if KB[item][1] + checkMines(agent_board, KB[item][0]) == KB[item][3]:
                        pass
                    else:
                        KB[item][1] = KB[item][3] - checkMines(agent_board, KB[item][0])


                check = False
                #check each item in the KB
                for item in KB:
                    #if clue is 0 all neighbors are safe
                    if item[1] == 0:
                        x = item
                        safeFringe += checkNeighbors(possible_moves, x[0])
                        check = True
                        break


                    #if number of neighbors is equal to tempClue, all are mines
                    elif item[1] == item[2]:
                        x = item
                        mineFringe += checkNeighbors(possible_moves, x[0])
                        check = True
                        break

                    #if neither of the two above things, don't do anything
                    else:
                        pass


                #only remove from KB if we added something to mine or safe fringe
                if check == True:
                    KB.remove(x)
                    continue

            '''
            #RANDOMPICK (LAST RESORT)
            '''

            #pick a random coordinate from the remaining possible moves
            x = random.randint(0,len(possible_moves) - 1)
            i = possible_moves[x][0]
            j = possible_moves[x][1]

            #open the random spot
            agent_board, coord, clue = updateBoard((i,j), main_board, agent_board)

            #if the spot we hit was a mine tell the user and keep going, no need to add to KB
            if clue == 9:
                pass

            #otherwise add to KB
            else:
                KB.append([coord, clue, len(checkNeighbors(possible_moves, coord)), clue])

            #remove from possible moves
            possible_moves.remove(coord)
            moveOrder.append((coord, clue))

BasicMinesweeper(15, 20)
BasicMinesweeper(15, 100)
