def MinesweeperRakshaa(main_board, agent_board, dim, n):
    import numpy as np
    
    #create our main board and the board the agent will see
    #main_board = environment(dim, n)
    #agent_board = environment(dim, 0) + 11

    #our three fringes, which make up our general knowledge base
    mineFringe = []
    safeFringe = []
    KB = []
    tot_mines = n

    #populate a list of all the possible moves we can make, which will keep track of moves that can be made
    possible_moves = []
    for i in range(0, dim):
        for j in range(0, dim):
            possible_moves.append((i, j))

    p = 9999
    
    #play until we finish the game
    gameFinished = False
    while gameFinished == False:
        #our terminating condition
        if len(possible_moves)==0:
            gameFinished=True
            
            clear_output()
            
            #UNCOMMENT TO SHOW BOARD OUTPUTS
            
            print("Agent's Board:")
            print(agent_board)
            print("The Actual Board:")
            print(main_board)
            
            #check our final score (# of correctly identified mines/# of total mines)
            total, correct = 0, 0 
            for i in range(0, dim):
                for j in range(0, dim):
                    if main_board[i][j] == 9:
                        total += 1
                    if agent_board[i][j] == 0.5:
                        correct += 1
            
            score = correct/total
            return score
        
        else:  
            p = float(tot_mines/len(possible_moves))
            
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
                    
                    #flag a spot with 0.5
                    agent_board[mineFringe[0][0]][mineFringe[0][1]] = 0.5
                    
                    #remove from possible moves and mine fringe
                    possible_moves.remove(mineFringe[0])
                    mineFringe.remove(mineFringe[0])
                    tot_mines -= 1
                    
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
                        
                    #show the recommened move
                    i = safeFringe[0][0]
                    j = safeFringe[0][1]
                    
                    #open a spot if it is in the safe fringe
                    agent_board, coord, clue = updateBoard((i,j), main_board, agent_board)
                    
                    #add move to KB, then remove from possible moves and mine fringe
                    #given the clue, calculate probability of neighboring squares having a mine
                    curr_p = clue/len(checkNeighbors(possible_moves, coord))
                    if curr_p < p:
                        p = curr_p
                    KB.append([coord, clue, len(checkNeighbors(possible_moves, coord)), clue, p])
                    possible_moves.remove(safeFringe[0])
                    safeFringe.remove(safeFringe[0])
                    
                #restarts main while loop from beginning
                continue

            '''
            #CHECK THE KNOWLEDGE BASE
            '''
            
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

                    
                    #updates the value of adjacent neighbors in the KB
                    KB[item][2] = len(checkNeighbors(possible_moves, KB[item][0]))
                    if KB[item][1] + checkMines(agent_board,KB[item][0]) == KB[item][3]:
                        pass
                    else:
                        KB[item][1] = KB[item][3] - checkMines(agent_board,KB[item][0])
            
                check = False
                #check each item in the KB
                for item in KB:
                    #if clue is 0 all neighbors are safe
                    if item[1] == 0: 
                        x = item
                        safeFringe += checkNeighbors(possible_moves, x[0]) 
                        check = True
                        break
                
                
                    #if number of neighbors is equal to clue, all are mines 
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
            moves_except_neighbors = []
            neighbors_with_least_p = []
            min_p = p
            
            #KB = [coord, clue, len(checkNeighbors(possible_moves, coord)), clue, p]
            
            #choose square with the least probability of having a mine
            #find mine that gives the least p for neighbors
            
            if len(KB) == 0:
                x = random.randint(0,len(possible_moves) - 1)
                i = possible_moves[x][0]
                j = possible_moves[x][1]
            
                #open the random spot
                agent_board, coord, clue = updateBoard((i,j), main_board, agent_board)
                
                curr_p = clue/len(checkNeighbors(possible_moves, coord))
                
                if curr_p < p:
                    p = curr_p
                KB.append([coord, clue, len(checkNeighbors(possible_moves, coord)), clue, p])
                continue
            
            for square in KB:
                print('square:', square)
                if square[4] <= min_p:
                    min_p = square[4]
                    i = square[0][0]
                    j = square[0][1]
                    print("i = ", i, ", j = ",j)
                    clue = square[1]
            #nothing was found that is better
            if min_p < p:
                #choose randomly from squares of least probability, given the number of mines adjacent to a square
                better_rand = (i,j) #mine
                print("agent board, coord= ", i, ", ", j)
                print(agent_board)
                neighbors_with_least_p = checkNeighbors(possible_moves, better_rand)
                if len(neighbors_with_least_p) == 0:
                    print("bad")
                    pass
                else:
                    r = random.randint(0,len(neighbors_with_least_p) - 1)
                    i = neighbors_with_least_p[r][0]
                    j = neighbors_with_least_p[r][1]
            
            #choose randomly from rest of the possible moves
            else:
                #pick a random coordinate from the other moves
                
                if(len(neighbors_with_least_p) == 0):
                    x = random.randint(0,len(possible_moves) - 1)
                    i = possible_moves[x][0]
                    j = possible_moves[x][1]
                    
                else:
                    for m in range(0, len(possible_moves)):
                        for n in range(0,len(neighbors_with_least_p)):
                            if possible_moves[m][0] != neighbors_with_least_p[n][0] and possible_moves[m][1] != neighbors_with_least_p[n][1]:
                                print('yes')
                                moves_except_neighbors.append(possible_moves[m])
                    r = random.randint(0,len(moves_except_neighbors)-1)
                    i = moves_except_neighbors[r][0]
                    j = moves_except_neighbors[r][1]
                    neighbors_with_least_p = checkNeighbors(possible_moves, (i,j))
                
            
            #open the chosen square
            agent_board, coord, clue = updateBoard((i,j), main_board, agent_board)
            
            #if the spot we hit was a mine tell the user and keep going, no need to add to KB
            if clue==9:
                pass
            
            #otherwise add to KB
            else:
                curr_p = clue/len(checkNeighbors(possible_moves, coord))
                if curr_p < p:
                    p = curr_p
                KB.append([coord, clue, len(checkNeighbors(possible_moves, coord)), clue, p])
            
            #remove from possible moves
            possible_moves.remove(coord)
