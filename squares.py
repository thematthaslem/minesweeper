import pygame as pg
import pygame.freetype
import math
import random

from collections import deque

class square(object) : 
    def __init__(self, id, width, top, left) : # Top: y-coord of top of square. Left: x-coord of left side

        self.id = id # col + row. Ex. col 2, row 3 -> 23

        self.type = 0   # -1: bomb
                         # 0: blank
                         # 1-8: number of bombs
       
        self.open = 0    # 0: not open
                         # 1: open
        
        self.width = width  # Width and Height of square

        self.left = left
        self.top = top
        self.right = left + width
        self.bottom = top + width

        self.numFont = pg.freetype.SysFont('fonts/Gamer.ttf', width * 0.7)

    #################
    ## Draw the square
    def drawSquare(self, screen) :
                
        textColor = (0,0,0)

        # If it's not open yet
        if self.open == 0 :
            pg.draw.rect(screen, (0,100,100), (self.left, self.top, self.width, self.width))
            pg.draw.rect(screen, (100,100,100), (self.left, self.top, self.width, self.width), 3)
            

        # If it is open
        if self.open == 1 :
            bgColor = (200, 200, 200)

            # If it's open and has a bomb
            if self.type == -1 : 
                bgColor = (255, 0, 0)
                
            # If it's open and is blank (has no number or anything)
            if self.type == 0 :
                bgColor = (150,150,150)

            # If it's open and has a number
            else :
                insideImg = self.numFont.render('0', True, (100,100,100)) # Text to show when the square is open

                # Define text Color
                if self.type == 1 : 
                    textColor = (0,0,250)
                if self.type == 2 :
                    textColor = (0, 200, 200)
                if self.type == 3 : 
                    textColor = (0, 250, 0)
                if self.type == 4 :
                    textColor = (250, 0, 0)
                if self.type > 4 :
                    textColor = (250, 0, 100)
                

            # Draw square and square outline
            pg.draw.rect(screen, bgColor, (self.left, self.top, self.width, self.width))
            pg.draw.rect(screen, (120,120,120), (self.left, self.top, self.width, self.width), 2)


            ###########################
            # Write text onto square
            #
            # If it has a number, show text
            if self.type > 0 :
                #.. Render text and surface 
                inside_text_surface, inside_text_rect = self.numFont.render(str(self.type), textColor)
                #.. Get text width and height (For centering number)
                text_width = inside_text_surface.get_width() 
                text_height = inside_text_surface.get_height()
                #.. Set center of text
                inside_text_rect.centerx = self.left + (self.width / 2)
                inside_text_rect.centery = self.top + (self.width / 2)
                #.. Show text
                screen.blit(inside_text_surface, inside_text_rect)
            #
            ############################


            ###########################
            # Show bomb
            #
            # If it has a -1, show text
            if self.type < 0 :
                #.. Get image
                bomb_img = pg.image.load('images/bomb.png')
                #.. Set image Size -> 70% of box size
                seventy_perc = self.width * 0.70
                bomb_width = int(seventy_perc)
                bomb_img = pg.transform.scale(bomb_img, (bomb_width, bomb_width))
                #.. Show image
                bomb_top = self.top + ((self.width - seventy_perc) / 2) # Top: top + half of 30%
                bomb_left = self.left + ((self.width - seventy_perc) / 2) # Left: Left + half of 30%
                screen.blit(bomb_img, (bomb_left, bomb_top) )
            #
            ############################
        



