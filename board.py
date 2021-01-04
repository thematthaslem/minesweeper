import pygame as pg
import pygame.freetype
import math
import random

from squares import square

from collections import deque


class board(object):
    def __init__(self, rows, columns, numBombs) :
        self.columns = columns 
        self.rows = rows

        self.screenWidth = 0
        self.screenHeight = 0

        self.squareWidth = 0.0

        self.squares = []
        self.squaresMap = {} # Dictionary to map a square's id to its index number in squares[] list
                             # Key => id
                             # Value => index
        self.bombs_list = []

        self.screenMargin = 30

        self.numBombs = numBombs




    # Setup/Initialize the board 
    def setup(self) : 

        # Get Square width 
        #.. Find smallest value of squareWidth
        #... screenHeight / rows 
        #... screenWidth / columns

        smallest = 0.0
        if (self.screenHeight / self.rows) < (self.screenWidth / self.rows) :
            smallest = ((self.screenHeight - (self.screenMargin * 2) ) / self.rows)
        else :
            smallest = ((self.screenWidth - (self.screenMargin * 2) ) / self.columns)


        # Save in board object
        self.squareWidth = smallest

        top = 0.0
        left = 0.0

        #########################
        # Set up Squares
        #
        # Make Square objects
        for i in range(self.rows) :
            top = (i * smallest) + self.screenMargin # top of square

            for j in range(self.columns) :
                left = (j * smallest) + self.screenMargin # Left of square
                tempId = (str(i) + 'x' + str(j)) # Squares id: row + x + column

                # Add square to list
                self.squares.append( square( tempId, smallest, top, left ) )
                # Add position of square to dictionary
                pos = len(self.squares) - 1 
                # If no items in list, make it the zero item
                if pos < 0 :
                    pos = 0
                self.squaresMap[tempId] = pos

        # Set up bomplacements
        bombCount = 0
        randomTemp = 0 # Random Number Temp
        squareCount = len(self.squares)

        while bombCount < self.numBombs : 
            randomTemp = random.randrange(0, squareCount)
            if not self.squares[randomTemp].type == -1 :
                self.squares[randomTemp].type = -1
                bombCount += 1
                # Place bombs in list 
                self.bombs_list.append(self.squares[randomTemp].id)
            else :
                continue

        #
        ######################################



        ##################################
        #   Set up numbers
        #
        #.. Set up queue to hold adjacent square id's
        id_queue = deque()
        #
        #.. Go through each bomb to get adjacent square Id's
        for bomb in self.bombs_list :
        #.. Get bomb's column and row
            bomb_id = bomb
            bomb_split = bomb_id.split('x')
            bomb_row = bomb_split[0]
            bomb_column = bomb_split[1]

        #
        #.. Get adjacent squares
            lower_range_row = int(bomb_row) - 1
            higher_range_row = int(bomb_row) + 1

            lower_range_column = int(bomb_column) - 1
            higher_range_column = int(bomb_column) + 1
            
        
            for i in range(lower_range_row, higher_range_row+1) : # i = row

                #Make sure it isn't zero or higher than number of columns/row
                if i < 0 or i == self.rows:
                    continue
                
                for j in range(lower_range_column, higher_range_column+1) : #j = column

                    #Make sure it isn't zero or higher than number of columns/row
                    if j < 0 or j == self.columns :
                        continue

                    temp_id = str(i) + "x" + str(j)
                    id_queue.append(temp_id)
        
        # Go thorugh queue
        while id_queue :
            temp_id = id_queue.popleft()

            # Get square 
            temp_square = self.get_square_from_id(temp_id)
            
            #Increase the squares type
            #.. Make sure it isn't a bomb
            if not temp_square.type == -1 :
                temp_square.type += 1
        #
        #####################
            



    #################################
    ## DRAW BOARD
    #################################
    def drawBoard(self, screen) :
        width = self.screenWidth - (self.screenMargin * 2) 
        height = self.screenWidth - (self.screenMargin * 2) 

        # Background
        pg.draw.rect(screen, (150,150,150), (self.screenMargin, self.screenMargin, width, height)) # Gray bg
        pg.draw.rect(screen, (90,90,90), (self.screenMargin, self.screenMargin, width, height), 5)  # Border


        # Squares
        for sq in self.squares :
            sq.drawSquare(screen)
            #pg.display.flip()



    ##########################################################
    ##
    ##              CHECK HIT
    ##      Check for a hit on squares
    ##
    ## -- calculate which Square was hit
    ## -- Show Square
    ## -- Calculate which squares to show if square was blank
    ## -- @TODO what happens when player steps on bomb
    ##
    ##########################################################
    def checkHit(self, xpos, ypos) :
        
        ############################
        ##
        ##  -- calculate which Square was hit
        ##  -- Show Square 
        ##

        # Find column number
        #.. (xpos/screenwidth) * numColumns --> (percentage of screen) * numColumns = which column they're on. (round down first) (subtract 1 to get to right one)
        column = math.floor( ( xpos / (self.screenWidth - (self.screenMargin * 2) ) ) * self.columns ) - 1
        row = math.floor( ( ypos / (self.screenHeight - (self.screenMargin * 2) ) ) * self.rows ) - 1
           
        squareId = str(row) + 'x' + str(column)

        # Find pos of square object in list. (Where it is in the array)
        pos = self.squaresMap[squareId]

        # Mark square as hit
        self.squares[pos].open = 1


        ############################
        ##
        ##  -- Calculate which squares to show if square was blank
        ##  -- Show those squares
        ##

        if self.squares[pos].type == 0 :

            # Queue for which squares to show (adjacent squares)
            ## Holds id of squares
            square_q = deque()

            # Add first square to queue 
            square_q.append(squareId)

            # Add every adjacent square to queue and every square adjacent to that
            while square_q :

                curr_square_id = square_q.popleft()
                curr_id_split = curr_square_id.split('x')
                curr_row = curr_id_split[0]
                curr_column = curr_id_split[1]

                curr_square = self.get_square_from_id(curr_square_id)

                # Show square
                curr_square.open = 1


                low_range_row = int(curr_row) - 1
                high_range_row = int(curr_row) + 1
            
                low_range_column = int(curr_column) - 1
                high_range_column = int(curr_column) + 1


                # If the square is not blank -> continue
                if not curr_square.type < 1 : 
                    continue



                # If the square is blank -> find adjacent squares
                for i in range(low_range_row, high_range_row+1) : # i: row
                    if i < 0 or i == self.rows : 
                        continue

                    for j in range(low_range_column, high_range_column + 1) :

                        # If column is off the grid -> continue
                        if j < 0 or j == self.columns :
                            continue

                        # Adjacent square id
                        new_id = str(i) + "x" + str(j)

                        # New square 
                        new_square = self.get_square_from_id(new_id)

                        # If new square is not already open -> add to queue
                        #if new_square.open == 0 :
                        if not new_id in square_q and new_square.open == 0 :
                            # Add to queue
                            square_q.append(new_id)






    ##########################################################
    ##
    ##              GET SQUARE
    ##      Get a square from id 
    ##
    ## -- Param: id of square chosen 
    ## -- Look from square_maps for position
    ## -- Use position to return selected square
    ##
    ##########################################################
    def get_square_from_id(self, id) :
        temp_pos = self.squaresMap[id]
        return self.squares[temp_pos]








