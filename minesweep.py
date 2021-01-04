import pygame as pg
import pygame.freetype

from board import *
from players import player

global SCREEN_WIDTH, SCREEN_HEIGHT

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600 

gameScreen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pg.display.set_caption("Minesweeper")

# Initialize font
pg.init()

def main() : 

    running = True
    clock = pg.time.Clock()

    # Set up board
    b = board(20, 20, 40)
    b.screenHeight = SCREEN_HEIGHT
    b.screenWidth = SCREEN_WIDTH
    b.setup()

    # Draw board first
    b.drawBoard(gameScreen)


    # Player
    p1 = player(SCREEN_WIDTH, SCREEN_HEIGHT, b)
    

    while running : 
        for event in pg.event.get() : 
            if event.type == pg.QUIT : 
                running = False

            p1.controls(event)

        b.drawBoard(gameScreen) # Draw board

        p1.draw(gameScreen)
        gameScreen.fill((20,200,10))

        clock.tick(60)

main()

pg.quit()

quit()