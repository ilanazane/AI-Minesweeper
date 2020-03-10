from MinesweeperMethods import *
from MinesweeperVisuals import game

'''
The Actual Game to be Played by our Agent

***********************INFERENCE****************************

**inputs:
dim = dimension size of the grid
n = number of mines

**returns:

'''

def AdvancedMinesweeper(dim, n):

    #create our main board and the board the agent will see
    main_board = environment(dim, n)
    agent_board = environment(dim, 0) + 11

    #our three fringes, which make up our general knowledge base
    mineFringe = []
    safeFringe = []
    KB = []

    #a list of the moves made in order to be used in pygame
    moveOrder = []

    #convert equation number to coordinate for inference
    dic1 = {}
    t = 0
    for i in range(dim):
        for j in range(dim):
            dic1[t] = (i,j)
            t += 1

    #convert coordinate to equation number for inference
    dic2 = {}
    t = 0
    for i in range(dim):
        for j in range(dim):
            dic2[(i,j)] = t
            t += 1

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
                to_be_removed = []
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
            #INFERENCE
            '''

            #take from knowledge base and add to an equation
            inference = []
            equals = []
            for item in KB:
                eq = equation(dim)
                x = checkNeighbors(possible_moves, item[0])
                for thing in x:
                    eq[dic2[thing]] = 1

                #append each equation to a general matrix
                inference.append(eq)
                #append the clue to a general matrix
                equals.append([item[1]])

            #the matrix solver
            if len(inference) == 0:
                pass
            else:
                #a list to make things easier in a later step
                index=list(range(len(inference)))
                #check through column
                for i in range(len(inference[0])):
                    #check through row
                    for row in range(len(inference)):
                        #this is for checking zero rows and columns
                        #looking for the first nonzero item in the row that has no nonzero to its left
                        if inference[row][i]!=0 and 1 not in inference[row][0:i]:

                            #scale the whole row by the leading nonzero item selected
                            scalar=1/inference[row][i]
                            for column in range(0,len(inference[0])):
                                inference[row][column]*=scalar
                            equals[row][0]*=scalar

                            #now do operations on every row but the one selected
                            for k in index[0:row]+index[row+1:]:

                                scalar2=inference[k][i]
                                for j in range(len(inference[0])):
                                    inference[k][j]=inference[k][j]-scalar2*inference[row][j]
                                equals[k][0]=equals[k][0]-scalar2*equals[row][0]

                gobackup=False

                #now perform a check on our matricies
                for i in range(len(inference)):

                    #counters to be used to check if an inference can be made
                    counter=0
                    negCounter=0

                    #check how many ones are in a row
                    for j in range(len(inference[i])):
                        if inference[i][j]==1:
                            counter+=1

                        #check for negative variables in the equation
                        elif inference[i][j] < 0:
                            negCounter+=1

                    #check if we have a definite safe move
                    if equals[i][0]==0 and counter > 0 and negCounter==0:
                        gobackup=True
                        for j in range(len(inference[i])):
                            if inference[i][j]==1:
                                safeFringe.append(dic1[j])

                    #check if we have a definite mine to flag
                    if counter == equals[i][0] and counter > 0 and negCounter==0:
                        gobackup=True
                        for j in range(len(inference[i])):
                            if inference[i][j]==1:
                                mineFringe.append(dic1[j])

                #if we made an inference, go back up
                if gobackup==True:
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

AdvancedMinesweeper(15, 20)
AdvancedMinesweeper(15, 100)
