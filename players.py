import pygame as pg

class player(object):
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, board) :  # board is actually the board object (for hitting Tiles)
        self.size_ratio = 0.75
        self.h = 30.0
        self.w = self.h * self.size_ratio

        

        self.posx = 0
        self.posy = 50

        self.speed = 3

        self.moveRight = False
        self.moveLeft = False
        self.moveUp = False
        self.moveDown = False

        self.jumpStatus = False
        self.poundStatus = False

        self.jumpStart = 0 # The position where jump started
        self.jumpPos = 0
        self.poundPos = 0 # Pretty much the speed of pound
        self.jumpDir = 0 # 0: up
                         # 1: down

        self.timer = 0 # General timer. Just increase in function and reset
        
        self.imgs = {
            'front': 'images/player/front.png',
            'left': 'images/player/left.png',
            'right': 'images/player/right.png',
            'back': 'images/player/back.png',
            'down-left': 'images/player/down-left.png',
            'down-right': 'images/player/down-right.png',
            'jump': 'images/player/jump.png',
            'jump-left': 'images/player/jump-left.png',
            'jump-right': 'images/player/jump-right.png',
            'pound': 'images/player/pound.png',
            'pound-right': 'images/player/pound-right.png',
            'pound-left': 'images/player/pound-left.png'
        }

        self.currImg = 'front' # Image if player is standing still

        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT

        self.board = board


##############################################
### DRAW THE PLAYER 
##############################################

    def draw(self, screen) :

        yHit = (self.posy + self.h) -4
        xHit = (self.posx + (self.w / 2)) # middle of the bottom of character

        pg.draw.rect(screen, (255,0,0), (xHit-5,yHit-5,10,10))

        ################
        # Control Boundaries. Make sure player can't move past screen
        ## dimensions
        charLeft = self.posx
        charRight = self.posx + self.w
        charTop = self.posy
        charBottom = self.posy + self.h 

        ## Make sure player isn't going to past screen
        if charLeft <= 0 : 
            self.moveLeft = False
        if charRight >= self.SCREEN_WIDTH :
            self.moveRight = False
        if charBottom >= self.SCREEN_HEIGHT :
            self.moveDown = False
        if charTop <= 0 : 
            self.moveUp = False


        
        #################
        # Show movement
        moveX = 0
        moveY = 0 

        if self.moveLeft :
            moveX = 0 - self.speed
        if self.moveRight : 
            moveX = self.speed 
        if self.moveUp : 
            moveY = 0 - self.speed
        if self.moveDown : 
            moveY = self.speed 

        # Show Jump
        if self.jumpStatus :

            # If at apex of jump, reverse direction
            if self.jumpPos <= -15 :
                self.jumpDir = 1
                self.jumpPos = 0
            # If back at ground, end jump 
            if self.jumpPos >= 15 :
                self.jumpDir = 0
                self.jumpPos = 0
                self.jumpStatus = False
                self.currImg = 'front'

            # Move jump up 
            if self.jumpDir == 0 :
                self.jumpPos -= 1
            # Move jump down
            if self.jumpDir == 1 :
                self.jumpPos += 1 

            moveY = self.jumpPos


        # Show Ground Pound
        if self.poundStatus :
            self.poundPos += 1 
            moveY = self.poundPos

            # If hit the ground after pound, 
            # turn off pound 
            # and activate hit square (square you pounded on)
            if self.posy >= self.jumpStart : 
                self.posy = self.jumpStart
                self.poundStatus = False
                self.poundPos = 0
                moveY = 0
                
                # Reset jump
                self.jumpPos = 0 
                self.jumpDir = 0

                # Hit square
                #.. Coordinates hit
                yHit = (self.posy + self.h)
                xHit = (self.posx + (self.w / 2)) - 6 # middle of the bottom of character and up 4

                # If jump outside of board, don't do anything
                if xHit < 30 or xHit > self.SCREEN_WIDTH - 30 or yHit < 30 or yHit > self.SCREEN_HEIGHT - 30 :
                    return
                else :
                    self.board.checkHit(xHit, yHit)
                    self.board.drawBoard(screen)


            



        self.posx += moveX
        self.posy += moveY



        img = pg.image.load(self.imgs[self.currImg])

        #############
        # Edit size 
        img = pg.transform.scale(img, ( int(self.w), int(self.h) ) ).convert_alpha()

        ##############
        # Show player
        screen.blit(img, (self.posx, self.posy))
        
        pg.display.flip()
        



##############################################
### MOVE CONTROLS 
##############################################

    ###################
    ### WALK
    ###################
    def controls(self, event) : 
        
        # Make sure key is being pressed or released
        if event.type == pg.KEYDOWN or event.type == pg.KEYUP :
            # Key being pressed or released
            key = event.key

            # If arrow keys, move
            if key == pg.K_LEFT or key == pg.K_RIGHT or key == pg.K_UP or key == pg.K_DOWN :
                self.walk(event)

            # If space key, jump
            if key == pg.K_SPACE :
                self.jump(event)
        
    
    def walk(self, event) :
        ###############
        # MOVEMENT
        ## If key down move 
        if event.type == pg.KEYDOWN :
            if event.key == pg.K_LEFT : 
                self.moveLeft = True
            if event.key == pg.K_RIGHT :
                self.moveRight = True
            if event.key == pg.K_UP :
                self.moveUp = True 
            if event.key == pg.K_DOWN :
                self.moveDown = True 

            

        ## If key up, stop moving
        if event.type == pg.KEYUP :
            if event.key == pg.K_LEFT : 
                self.moveLeft = False
            if event.key == pg.K_RIGHT :
                self.moveRight = False
            if event.key == pg.K_UP :
                self.moveUp = False 
            if event.key == pg.K_DOWN :
                self.moveDown = False 


        ##############
        # Choose which image to show.
        ## Ex: if walking down, show front 
        imgName = self.currImg
        if self.moveLeft :
            imgName = 'left'
        if self.moveRight :
            imgName = 'right'
        if self.moveDown :
            imgName = 'front'

            if self.moveRight : 
                imgName = 'down-right'

            if self.moveDown and self.moveLeft : 
                imgName = 'down-left'

        if self.moveUp :
            imgName = 'back'

        self.currImg = imgName


    ###################
    ### JUMP
    ###################
    def jump(self, ev) :

        # If spacebar is being pressed
        if ev.type == pg.KEYDOWN :
            
            # If currently doing ground pound, do do nothing
            if self.poundStatus :
                return

            # If not already jumping, jump
            elif not self.jumpStatus :
                self.moveDown = self.moveUp = self.moveLeft = self.moveRight = False
                self.jumpStatus = True
                self.currImg = 'jump'
                self.jumpStart = self.posy


            # If already jumping, do the ground pound 
            else :
                self.jumpStatus = False
                self.poundStatus = True
            
                self.currImg = 'pound'
                


        

   
            

