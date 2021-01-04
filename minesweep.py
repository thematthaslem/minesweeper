import pygame as pg
import pygame.freetype

from board import *
from players import player

# Initialize font
pg.init()

global SCREEN_WIDTH, SCREEN_HEIGHT

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600 

font_gamer = pg.freetype.SysFont('fonts/Gamer.ttf', 20)

gameScreen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pg.display.set_caption("Minesweeper")



def main() : 

    running = True
    clock = pg.time.Clock()

    # Set up board
    b = board(20, 20, 40)
    b.screenHeight = SCREEN_HEIGHT
    b.screenWidth = SCREEN_WIDTH
    b.setup()

    # Create board surface
    board_surface = pg.Surface( (b.board_width, b.board_height) )

    # Draw board on Surface
    b.drawBoard(board_surface)

    # Create Score Surface
    score_surface = pg.Surface( (100, 50), pg.SRCALPHA )
    


    # Player
    p1 = player(SCREEN_WIDTH, SCREEN_HEIGHT, b)
    

    while running : 
        for event in pg.event.get() : 
            if event.type == pg.QUIT : 
                running = False

            p1.controls(event)

        

        #b.drawBoard(gameScreen) # Draw board
        # The board is updated every time player uses ground pound
        # Draw Board
        gameScreen.blit(board_surface, (b.screenMargin, b.screenMargin) )

        # Draw Player
        p1.draw(gameScreen, board_surface)

        # Draw Score
        score_text_surface, score_text_rect = font_gamer.render("Score: " + str(p1.score), (30,30,30))
        score_text_rect.top = 10
        score_text_rect.left = 10
        gameScreen.blit(score_text_surface, score_text_rect)

        # Draw Lives
        lives_text_surface, lives_text_rect = font_gamer.render("Lives: " + str(p1.lives), (30,30,30))
        lives_width = lives_text_surface.get_width()
        lives_text_rect.top = 10
        lives_text_rect.left = SCREEN_WIDTH - lives_width - 10
        gameScreen.blit(lives_text_surface, lives_text_rect)

        pg.display.flip()

        gameScreen.fill((20,200,10))

        clock.tick(60)

main()

pg.quit()

quit()