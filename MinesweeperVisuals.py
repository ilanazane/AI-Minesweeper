import pygame
import time
from MinesweeperMethods import *

'''
The pygame GUI that does not allow for user inputs

**inputs:
size = size of the grid
grid_main = the main grid to check against
grid = the grid to be updated and displayed
moveOrder = the order of moves that the AI solved our maze with

**returns:
Nothing (just visuals)
'''

def game(size, grid_main, grid, moveOrder):
    #Some colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREY = (200,200,200)

    #Set the Height and Width of our grid cells
    WIDTH = size*2
    HEIGHT = size*2
    MARGIN = 5

    #Show the main grid in the terminal
    print(grid_main)

    #Start up pygame
    pygame.init()

    #load in our images
    flag_img = pygame.image.load("Flag.png")
    flag_img = pygame.transform.scale(flag_img, (WIDTH,HEIGHT))
    bomb_img = pygame.image.load("bomb.png")
    bomb_img = pygame.transform.scale(bomb_img, (WIDTH,HEIGHT))

    #Set our font
    font = pygame.font.SysFont("comicsansms", 12)

    #Set the Window Size
    WINDOW_SIZE = [WIDTH*size + MARGIN*(size + 1), HEIGHT*size + MARGIN*(size + 1)]
    screen = pygame.display.set_mode(WINDOW_SIZE)

    #The title of our game
    pygame.display.set_caption("Minesweeper AI")

    #Used for the update rate of the visuals
    clock = pygame.time.Clock()


    first_update = 0
    update = []

    #run until we are through our move list
    while len(moveOrder) > 0:
        #the first display check: we don't want it to clear the text display each time
        if first_update == 0:
            pygame.display.flip()

        click = False

        #check if the user quit the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True


        click = True
        first_update += 1
        row = moveOrder[0][0][0]
        column = moveOrder[0][0][1]
        grid[row][column] = moveOrder[0][1]
        moveOrder.remove(moveOrder[0])

        #check what image to update the game with; either a flag, bomb, or number
        if grid[row][column] == 9:
            text = font.render("bomb", True, (0,0,0))
            update.append((bomb_img, (MARGIN+WIDTH)*(column)+WIDTH/2 - 2*MARGIN, (MARGIN+HEIGHT)*(row)+MARGIN/2 + (1/2)*MARGIN))
        elif grid[row][column] == 0.5:
            text = font.render("flag", True, (255,0,0))
            update.append((flag_img, (MARGIN+WIDTH)*(column)+WIDTH/2 - 2*MARGIN, (MARGIN+HEIGHT)*(row)+MARGIN/2 + (1/2)*MARGIN))
        else:
            text = font.render(str(int(grid[row][column])), True, (0,0,0))
            update.append((text, (MARGIN+WIDTH)*(column)+WIDTH/2, (MARGIN+HEIGHT)*(row)+MARGIN/2 + MARGIN))


        #Now begin to draw the game board
        screen.fill(BLACK)
        for row in range(size):
            for column in range(size):
                color = WHITE
                if grid[row][column] == 9:
                    color = RED
                elif grid[row][column] == 0.5:
                    color = GREY
                elif grid[row][column] == 11:
                    pass
                else:
                    color = GREY

                pygame.draw.rect(screen,color,[(MARGIN + WIDTH) * column + MARGIN,(MARGIN + HEIGHT) * row + MARGIN,WIDTH,HEIGHT])

        if click:
            for item in update:
                screen.blit(item[0], (item[1], item[2]))
            pygame.display.flip()

        #Frame rate
        clock.tick(60)

    #this is so the game hangs around until the user quits out of the window to see the end results
    yes = True
    while yes:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                yes = False

    pygame.quit()
