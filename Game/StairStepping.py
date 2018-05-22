import pygame
import sys
import random

movementSpeed = 2 #speed the char moves at
movementSpeedConstant = 2

gravity = 0.09

movingScreenCONSTANT = 1.0 #do not change this, used so the below variable can be changed easily
movingScreenSpeed = 1.0 #holds the value to move the platforms by, 0 to stop moving

speedDeadlyObjectRange = (3,7) #this is the range of speeds for the deadly falling objects
speedHelpfulObjectRange = (3,7) #this is the range for the helpful objects that fall


multScore = 2 #multiply the score by this when the player gets a score multiplying item

#images:
#player stances
rightStance = "../Resources/Images/rightStance.png"
leftStance = "../Resources/Images/leftStance.png"
rightJump1 = "../Resources/Images/jump right_1.png"
rightJump2 = "../Resources/Images/jump right_2.png"
leftJump1 = "../Resources/Images/jump left_1.png"
leftJump2 = "../Resources/Images/jump left_2.png"
rightMove1 = "../Resources/Images/moveRight1.png"
rightMove2 = "../Resources/Images/moveRight2.png"
leftMove1 = "../Resources/Images/moveLeft1.png"
leftMove2 = "../Resources/Images/moveLeft2.png"

#array to hold the animation for left move and right move
leftMoveAnimation = [leftMove1, leftMove2, leftMove1]
rightMoveAnimation = [rightMove1, rightMove2, rightMove1]

#platform images
p1 = "../Resources/Images/Platform 1.png"
p2 = "../Resources/Images/Platform 2.png"
p3 = "../Resources/Images/Platform 3.png"
p4 = "../Resources/Images/Platform 4.png"
#p5 = "../Resources/Images/Platform_YOU_THERE.png"


#teleportation images
#t1 and t2 will appear where the sprite is being teleported from
#t3-t5 will appear at the destination of the teleportation
t1 = "../Resources/Images/teleport_1.png"
t2 = "../Resources/Images/teleport_2.png"
t3 = "../Resources/Images/teleport_3.png"
t4 = "../Resources/Images/teleport_4.png"
t5 = "../Resources/Images/teleport_5.png"
#array to store different teleportation sprites
teleport_images = [t1, t2, t3, t4, t5]


backgroundImage = "../Resources/Images/BG 1.jpg" #background during gameplay
backgroundImage2 = "../Resources/Images/BG 1.jpg"
platformImage = "../Resources/Images/platform.png" 

playAgainImage = "../Resources/Images/playAgain.png"#play again image path
exitGameImage = "../Resources/Images/exitGame.jpg" #exit game image path
mainStartImage = "../Resources/Images/startGame.png" #start game image path

mainMenuImage = "../Resources/Images/mainMenu.png" #shows the main menu image

gameoverImage = "../Resources/Images/gameover2.jpg" #shows game over menu image

#bad object(s)
numBadObjs = 7
fallingObject1 = "../Resources/Images/eyeballFalling2.png" #this object falls "randomly"
fallingObject2 = "../Resources/Images/poisonBottle.png" #this object falls "randomly"
fallingObject4 = "../Resources/Images/enemyBloodCell.png"
fallingObject5 = "../Resources/Images/enemyBacteria.png"
fallingObject7 = "../Resources/Images/Virus Green.png"
fallingObject8 = "../Resources/Images/Virus Purple.png"
fallingObject9 = "../Resources/Images/Virus Red.png"

#array that stores different platform images
platforms = [p1, p2, p3, p4]

fBADObjectArray = [fallingObject1, fallingObject2, fallingObject4, fallingObject5, fallingObject7, fallingObject8, fallingObject9]

#good object
numGoodObjs = 2
fallingObject3 = "../Resources/Images/x2-logo.png" #good object, doubles score
fallingObject6 = "../Resources/Images/increasedSpeedPowerup.png" #increases speed of player for a little bit

fGOODObjectArray = [fallingObject3, fallingObject6]

#simple class that allows an image to be clicked on, used for the playAgain and exitGame pictures at Game Over screen
class clickableImage:
    def __init__(self, x=0, y=0, imgPath="", nameStr=""):
        self.x = x
        self.y = y

        self.nameStr = nameStr #simply holds what the image is called in the code

        self.imgPath = imgPath
        self.img = pygame.image.load(imgPath)

        self.imgRect = self.img.get_rect() #< xPos, yPos, WidthRect, HeightRect> of rectangle
        self.imgRect.x = self.x
        self.imgRect.y = self.y
           
    def clickCheck (self, event):
        if self.imgRect.collidepoint(event):
            return True #mouse click is colliding with the image rectangle
        return False
    def draw(self, screen):
       screen.blit(self.img, (self.x, self.y))


class vector2:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    def xy (self):
        return (self.x, self.y)
    def add (self, v2):
        result = vector2()
        result.x = self.x + v2.x
        result.y = self.y + v2.y
        return result

#this class acts as the holder for the falling object, easier than modifying the already insane sprite class.
class fallingObjectClass:
    def __init__(self, px, py, img = "", vx=0, vy = 0, harmful=False, multiplier=0, speedBoost=False):
        self.harmful = harmful #can kill player or help them?

        self.loc = vector2(px, py)
        self.img = pygame.image.load(img)

        self.imgRect = self.img.get_rect()
        self.imgSize = pygame.Surface.get_size(self.img) #determines the size of the image
        self.imgSize = vector2(self.imgSize[0], self.imgSize[1])

        self.radius = self.imgSize.y/2

        self.v = vector2(vx, vy)
        self.multiplier = multiplier #holds value to multiply the score by

        self.speedBoost = speedBoost

    def updateObject(self, screen):
        self.loc = self.loc.add(self.v)

        #update rectangle
        self.imgRect.x = self.loc.x
        self.imgRect.y = self.loc.y

        if (self.loc.y >= HEIGHT): #off screen, thus delete
            #del self
            fallingObjectArray.remove(self)
        else:
            self.drawEnemy(screen)
    def drawEnemy (self, screen):
        #circle = pygame.draw.circle(screen, (255,255,0), (int(self.loc.x) + self.imgSize.x/2, int(self.loc.y) + self.imgSize.y/2), self.radius, 5)
        screen.blit(self.img, self.loc.xy()) 
    def collidePlayer(self, alive, scoreMult): #still horrible collision detecting
        scoreMult = 0
        speed = 0

        if (self.harmful == True): #kill the player!
            alive = False
        elif (self.speedBoost == False and self.harmful == False):
            scoreMult = self.multiplier #multiply the score later
        elif (self.speedBoost == True): #increase movement speed!
            speed = 1

        fallingObjectArray.remove(self) #now delete the object
        return (alive, scoreMult, speed) #returns all three values

        """tmp1 = pygame.Surface( (IMG_WIDTH,IMG_HEIGHT), pygame.SRCALPHA )
        tmp1.blit( img, (0,0), area=mask )
        m1 = pygame.mask.from_surface( tmp1 )

        tmp2 = pygame.Surface( (IMG_WIDTH,IMG_HEIGHT), pygame.SRCALPHA )
        tmp2.blit( img, (0,0), area=mask )
        m2 = pygame.mask.from_surface( tmp2 )

        if m1.overlap( m2, (300-loc.x,300-loc.y) ) is not None:
            print "BOOM!"
"""

#this class is used for the player and the platform objects, each has different functions it uses
class sprite:
    def __init__(self, px=0, py=0, img = "", vx=0, vy=0): 
        self.loc = vector2(px, py)
        self.img = pygame.image.load(img) #loads image from the string passed in

        self.imgSize = pygame.Surface.get_size(self.img) #determines the size of the image
        self.imgSize = vector2(self.imgSize[0], self.imgSize[1])

        self.imgRect = self.img.get_rect() #< xPos, yPos, WidthRect, HeightRect> of rectangle
        self.imgRect.x = self.loc.x
        self.imgRect.y = self.loc.y

        #save the current image of the sprite for future reference
        self.current_state = img

        self.v = vector2(vx,vy)

        self.radius = self.imgSize.y/2

        self.onPlatform = True #determines whether or not to use gravity at the time
        
        #ADDED: keep track of which block the player is on; "jump" keeps track of when the player is jumping
        self.on = False
        self.jump = False

        self.gavePoint = False #for platforms

        self.isMonster = False


    def moveSprite(self, key, leftIterator, rightIterator):
        #keys = pygame.key.get_pressed()
        #print "pressing left: ", keys[pygame.K_LEFT]
        #print "pressing right: ", keys[pygame.K_RIGHT]
        #print "pressing space: ", keys[pygame.K_SPACE]


        #ADDED: second condition so that you can only jump when you're on a platform as well as "jump" value
        if (key == pygame.K_SPACE) and (self.onPlatform == True):
            #check the direction the player is in
            #in order to jump according to that direction
            if self.current_state == rightStance:     #if right stance
                self.img = pygame.image.load(rightJump1)
                self.current_state = rightJump1
                
            elif self.current_state == leftStance:
                self.img = pygame.image.load(leftJump1)
                self.current_state = leftJump1
            
            #space bar pressed, jump!
            self.onPlatform = False
            self.jump = True

        #ADDED: instead of adding to the current velocity of the player (which may be affected by gravity), make the jump always the same height
            self.v = vector2(self.v.x, -4)

        if (key == pygame.K_RIGHT or key == pygame.K_d):
        #ADDED: change image accordingly
            if self.onPlatform == True:
                self.img = pygame.image.load(rightStance)
                #update the status of the sprite
                self.current_state = rightStance

#ADDED: WORKS!!
            else:   #in case the player is in the air
                if self.current_state == leftJump1:
                    self.img = pygame.image.load(rightJump1)
                    self.current_state = rightJump1
                elif self.current_state == leftJump2:
                    self.img = pygame.image.load(rightJump2)
                    self.current_state = rightJump2
#######
            self.v = self.v.add(vector2(movementSpeed, 0) )
            
        if (key == pygame.K_LEFT or key == pygame.K_a):
        #ADDED: change image accordingly
            if self.onPlatform == True:
                self.img = pygame.image.load(leftStance)
                #update the status of the sprite
                self.current_state = leftStance

#ADDED:  WORKS!!
            else:   #in case the player is in the air
                if self.current_state == rightJump1:
                    self.img = pygame.image.load(leftJump1)
                    self.current_state = leftJump1
                elif self.current_state == rightJump2:
                    self.img = pygame.image.load(leftJump2)
                    self.current_state = leftJump2
#######
            self.v = self.v.add(vector2(-movementSpeed, 0) )
        return leftIterator, rightIterator
            

            
    def stopMovingSprite(self, key):
        if (key == pygame.K_RIGHT or key == pygame.K_d):
            self.v.x = 0
            if (self.onPlatform == True):
                self.img = pygame.image.load(rightStance)
                self.current_state = rightStance
        if (key == pygame.K_LEFT or key == pygame.K_a):
            self.v.x = 0
            if(self.onPlatform == True):
                self.img = pygame.image.load(leftStance)
                self.current_state = leftStance
    
        #ADDED: second condition and jump variable which will indicate when the player is allowed to jump
        if (key == pygame.K_SPACE and self.jump == True):
            #self.v.y = 0 
            self.onPlatform = False
            self.jump = False

    def draw(self,screen):
        #rect = pygame.draw.rect(screen, (255,255,0), self.imgRect, 5)
        screen.blit( self.img, self.loc.xy() )

    def drawEnemy (self, screen):
        #circle = pygame.draw.circle(screen, (255,255,0), (int(self.loc.x) + self.imgSize.x/2, int(self.loc.y) + self.imgSize.y/2), self.radius, 5)
        screen.blit(self.img, self.loc.xy()) 
    def updatePlatform(self, screen):
        self.loc = self.loc.add(self.v)

        #update rectangle
        self.imgRect.x = self.loc.x
        self.imgRect.y = self.loc.y

        if (self.loc.y >= HEIGHT): #off screen, thus delete
            #del self
            platformArray.remove(self)
        else:
            self.draw(screen)
    def updateObject(self, screen):
        self.loc = self.loc.add(self.v)

        #update rectangle
        self.imgRect.x = self.loc.x
        self.imgRect.y = self.loc.y

        if (self.loc.y >= HEIGHT): #off screen, thus delete
            #del self
            fallingObjectArray.remove(self)
        else:
            self.drawEnemy(screen)
    
    def movePlayer (self, x, y, score):
        self.loc = self.loc.add(vector2(x, y))

        for platform in platformArray:
            if (self.imgRect.colliderect(platform.imgRect)): #if rectangle is colliding:

                #check if hitting the top of the platform, or bottom
                dif = self.imgRect.bottom - platform.imgRect.top #find how far apart the player bottom is from the top of the platform
                bottomDif = self.imgRect.top - platform.imgRect.bottom #find how far apart the player top is from the bottom of the platform
              
                leftPlatDif = self.imgRect.right - platform.imgRect.left;
                rightPlatDif = self.imgRect.left - platform.imgRect.right;

                if dif <= 5 and dif >= -5: #means hitting the top of the platform, chose 5 because that seemed reasonable at the time
                    if self.v.x >= 0 or self.v.x < 0: #and moving left or right...
                        self.onPlatform = True #means stop using gravity, move at the constant speed the platform is moving at
                        platform.on = True
#CHANGE MADE HERE: SEEMS TO WORK TO CHANGE BACK TO NORMAL SPRITE WHEN LANDING ON PLATFORM
                        #load image of landing according to direction
                        if self.current_state == leftJump1 or self.current_state == leftJump2:
                            self.current_state = leftStance
                            self.img = pygame.image.load(leftStance)
                        elif self.current_state == rightJump1 or self.current_state == rightJump2:
                            self.current_state = rightStance
                            self.img = pygame.image.load(rightStance)
###################
                        if (platform.gavePoint == False):
                            score += 5
                            platform.gavePoint = True

                        self.imgRect.y = platform.imgRect.top - self.imgRect.height   #set the rectangle of player to be the top, minus the height of the sprite
                        self.loc.y = self.imgRect.y #set the location to the player rectangle
                        self.v.y = 0 #make player stop moving
                
                elif bottomDif <= 5 and bottomDif >= -5: #tests if the player is hitting the bottom of a platform, while moving too
                    if self.v.x >= 0 or self.v.x < 0:
                        self.imgRect.y = platform.imgRect.bottom  #set the rectangle of player to be the bottom of platform
                        self.loc.y = self.imgRect.y #set the location to the player rectangle
                        self.v.y = -self.v.y #make player bounce off platform bottom
                        if self.v.y == 0:
                            self.v.y = -1

                elif leftPlatDif <= 5 and leftPlatDif >= -5:
                    if self.v.x >= 0 or self.v.x < 0: # Moving right; Hit the left side of the wall
                        self.imgRect.x = platform.imgRect.left  - self.imgSize.x #set the rectangle of player to be the left, minus the size of the sprite
                        self.loc.x = self.imgRect.x #set the location to the player rectangle
                        #self.v.x = self.v.y = 0 #make player stop moving
            
                elif rightPlatDif <= 5 and rightPlatDif >= -5:
                    if self.v.x < 0 or self.v.x >= 0: # Moving left; Hit the right side of the wall
                        self.imgRect.x = platform.imgRect.right  #set the rectangle of player to be the right of platform
                        self.loc.x = self.imgRect.x #set the location to the player rectangle
                        #self.v.x = self.v.y = 0 #make player stop moving

                else: #catch all statement, going too fast, going right through platform, this fixes it
                    if self.v.x >= 0 or self.v.x < 0: #and moving left or right...
                        self.onPlatform = True #means stop using gravity, move at the constant speed the platform is moving at
                        platform.on = True

                        if (platform.gavePoint == False):
                            score += 5
                            platform.gavePoint = True

                        self.imgRect.y = platform.imgRect.top - self.imgRect.height   #set the rectangle of player to be the top, minus the height of the sprite
                        self.loc.y = self.imgRect.y #set the location to the player rectangle
                        self.v.y = 0 #make player stop moving


        return score


    def updatePlayer(self, screen, alive, score):
        #check if the player is on a platform
       #ADDED: check if the player is on top of the platform right before applying gravity
        for platform in platformArray:
            if (platform.on == True and self.loc.x + self.imgRect.width < platform.imgRect.x) or (platform.on == True and self.loc.x > platform.imgRect.x + platform.imgRect.width):
                self.onPlatform = False
                platform.on = False
        if self.onPlatform == False:
            self.v = self.v.add(vector2(0, gravity) )

        speedWasBoosted = False #to determine if the player got a speed boosting powerup or not

        #added to test for collision with falling object
        for object in fallingObjectArray:
            if self.imgRect.colliderect(object.imgRect):
                global movementSpeed
                mult = 0
                speedBoost = 0
                (alive, mult, speedBoost) = object.collidePlayer(alive, mult)
                
                if mult != 0:
                    score *= mult
                if (speedBoost != 0):
                    speedWasBoosted = True
                    movementSpeed += 1 #increments the variable used to determine how much to speed up the player

        #self.loc = self.loc.add(self.v)
        score = self.movePlayer(self.v.x, 0, score) #moves player in each direction seperately, supposedly helps with the collision or something I read
        score = self.movePlayer(0, self.v.y, score)

        if (self.onPlatform == True): #if the player is on a platform, move the player according to the speed of the screen
            self.loc.y += movingScreenSpeed

        if (self.loc.x >= WIDTH - self.imgSize.x):
            #going to right of screen
            self.loc.x = WIDTH - self.imgSize.x #set loc to be not into the wall, just hitting it
        if (self.loc.x <= 0 ):
            #going to left of screen
            self.loc.x = 0 #just hitting wall, not into it
        if (self.loc.y >= HEIGHT - self.imgSize.y):
            #going bottom of screen
            self.loc.y = HEIGHT - self.imgSize.y
            self.onPlatform = True

            #bottom of screen means death:
            alive = False
        if (self.loc.y <= 0 ):
            #going top of screen
            self.loc.y = 0
        #update rectangle
        self.imgRect.x = self.loc.x
        self.imgRect.y = self.loc.y


        self.draw(screen)
        return (alive, score, speedWasBoosted) #if the player hit the bottom of the screen or not, have to return, cannot modify it any other way

#this function will show the main menu if and only if the player is just starting the game
def showMainMenu(screen, show):
    while show:
        #show main menu, allow player to play, exit

        pygame.event.pump()
        screen.blit(mainMenu, (0,0) ) #blit the image

        for evt in pygame.event.get():
            if (evt.type == pygame.QUIT):
                pygame.quit()
                sys.exit()
            if evt.type == pygame.MOUSEBUTTONDOWN:  
                if evt.button == 1: #if left button was clicked...
                    for object in mainMenuImages: #check which picture was hit, either playAgain, exit, or neither
                        pressed = object.clickCheck(evt.pos)
                        if (pressed == True and object.nameStr == "Start Game"):
                            #now start the game
                            show = False
                        elif (pressed == True and object.nameStr == "Exit Game"):
                            pygame.quit()
                            sys.exit()
        for img in mainMenuImages:
            img.draw(screen)
        pygame.display.flip()
    return show

def showGameOverMenu(screen):
    pygame.event.pump()
    
    screen.blit(gameOverIm, (0,0)) #show the gameover background
    screen.blit(scoreText, (0,0)) #show the final ending score text at top left of the screen

    for img in imageList: #draw the images of the play again and exit images
        img.draw(screen)
        
    for evt in pygame.event.get():
        if (evt.type == pygame.QUIT):
            pygame.quit()
            sys.exit()
        if evt.type == pygame.MOUSEBUTTONDOWN:  
            if evt.button == 1: #if left button was clicked...
                for object in imageList: #check which picture was hit, either playAgain, exit, or neither
                    pressed = object.clickCheck(evt.pos)
                    if pressed == True and object.nameStr == "Play Again":
                        return 1 #stop showing the main menu, and go back to game
                    elif pressed == True and object.nameStr == "Exit Game":
                        alive = False #this exits the inner loop and outer loop, thus exiting the game
                        repeat = False
                        pygame.quit() #added due to crashing??
                        sys.exit()
                
    pygame.display.flip()


#this function will create a falling object. Uses score and random numbers to determine if anything should be added to fallingObjectArray
def createFallingObject(score, playerObject):
    objectLoc = (0,0)

    rNum = random.randint(0, 9) #gen random num from 0 to 9

    #60% chance of creating bad object, but if score is over 100, 70%, and if score is over 200, then it is upped to 80% chance, 90% if score > 400
    if rNum < 6 or (score > 100 and rNum == 6) or (score > 200 and rNum == 7) or (score > 400 and rNum == 8): 
        objectLoc = (playerObject.loc.x-playerObject.imgSize.x/2, -10)
        randomVelY = random.randint(speedDeadlyObjectRange[0], speedDeadlyObjectRange[1])

        #now determine which of the objects to use for the deadly falling object image:
        randomBadObjectSelection = random.randint(1, numBadObjs)

        badObjStr = fBADObjectArray[randomBadObjectSelection-1]

        fallingObjectArray.append(fallingObjectClass(objectLoc[0], objectLoc[1], badObjStr, 0, randomVelY, True, 0))

    elif rNum == 9: #10 percent chance of creating good object
        objectLoc = (WIDTH-playerObject.loc.x, -10)
        randomVelY = random.randint(speedHelpfulObjectRange[0], speedHelpfulObjectRange[1]) #select a random vel from tuple containing speeds

        #now determine which of the good falling objects will fall:
        randomGoodObjectSelection = random.randint(1, numGoodObjs)

        goodObjStr = fGOODObjectArray[randomGoodObjectSelection-1]

        if (randomGoodObjectSelection-1 == 0): #this is the x2 image multiplier
            fallingObjectArray.append(fallingObjectClass(objectLoc[0], objectLoc[1], goodObjStr, 0, randomVelY, False, 2))

        elif (randomGoodObjectSelection-1 == 1): #this is the increased speed for the player
            fallingObjectArray.append(fallingObjectClass(objectLoc[0], objectLoc[1], goodObjStr, 0, randomVelY, False, 0, True))


#now begins the game section of the code
pygame.init()

#constants
WIDTH = 800
HEIGHT = 600

#teleportation lightning###############
teleportation = sprite(0, 0, teleport_images[0], 0, 0)
#######################################

#####################MUSIC
pygame.mixer.music.load("../Resources/Sounds/Broken_reality.wav")
t_effect = pygame.mixer.Sound("../Resources/Effects/teleport_effect.wav")
##########################


#animation variables;deal with time frames
frame = 0
frame_timer = 0
FRAME_TIME = 50    
FRAME_CT = 2   #two images to iterate over

#create the button images
playAgainButton = clickableImage(150, 50, playAgainImage, "Play Again")
exitImage = clickableImage(450, 50, exitGameImage, "Exit Game")

imageList = (playAgainButton, exitImage)

gameOverIm = pygame.image.load(gameoverImage) #could have used the sprite class, not really needed though

#ADDED: main menu stuff
mainMenu = pygame.image.load(mainMenuImage)

#create main menu pictures:
mainStart = clickableImage(150, 100, mainStartImage, "Start Game")

mainExit = clickableImage(450, 100, exitGameImage, "Exit Game")

#create array to hold the starting images:
mainMenuImages = [mainStart, mainExit] 
#end ADDED main menu stuff

#start location for player
playerStart = vector2(0,HEIGHT-199)

#create array to hold all platform objects:
platformArray = []


#create playerObject
playerObject = sprite(playerStart.x, playerStart.y, rightStance, 0, 0)

#starting location for starting platform, where the player will start the game at:
platformStart = vector2(0, HEIGHT-200 + playerObject.imgSize.y)


#now create the first platform of the game, so the player can start there:
platformArray.append(sprite(platformStart.x, platformStart.y, platforms[random.randint(0, len(platforms) - 1)], 0, movingScreenSpeed) )


screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
screen.fill((255, 255 ,0))

pygame.display.set_caption( "Comatose" ) #set the name of the Game


#create background object
background = sprite(0,0,backgroundImage, 0,0)
background.loc.y = -background.imgSize.y + HEIGHT
background2 = sprite(0,0,backgroundImage2, 0,0)
background2.loc.y = -background2.imgSize.y - background.imgSize.y + HEIGHT

#create a score text object and variable to count it:
scoreCount = -5
font = pygame.font.Font(None, 40) #font size is last number on this line
scoreText = font.render(str("Score: %s" % scoreCount), 1, (255, 0,0))


y = 0
alive = True
repeat = True

#keep track of power-ups: "slow time" & "teleport"
p_times = 3             #only 3 slow-down the platforms
p_time_bool = False     #power starts out "not ocurring"
timer = 0               #timer for how long the power lasts
t_times = 3             #only 3 teleports

##################################
teleport = False  
##################################


#ADDED:
#create a variable to show the main menu if and only if the game was just started
iteration = 1

#create a variable to hold the amount of time to wait until the game starts upon hitting start game
seconds = 3 #wait 3 seconds
milliseconds = 0.0
canStart = False

#ADDED: keep track of the powerups left for the player to use
p_font = pygame.font.Font(None, 40)
p_text = font.render(str("Slow-mo: %s" % p_times), 1, (0, 0, 255))
slowDownTime = 5 #slow platforms for 5 seconds
t_font = pygame.font.Font(None, 40)
t_text = font.render(str("Teleports: %s" % t_times), 1, (255,255, 255))

#ADD ON 2.5: flying objects stuff
fallingObjectArray = []
platformCount = 0 #when it gets to 2+, create a new falling object

#added for main menu:
show = True

#######################
delta = 0
target_x,target_y = 0,0
t = 0
#######################
pygame.mixer.music.play(-1)

while repeat: #outer loop repeats after end of game, exits if player decides to exit, or repeat if playing again
    show = showMainMenu(screen, show)

    speedWasBoosted = False #for powerup to determine if movement speed increased or not
   #Reset powerups usage
    p_times = 3             #reset to 3 "slow time"
    p_time_bool = False     #power starts out "not ocurring"
    timer = 0               #timer for how long the power lasts
    slowDownTime = 5
    t_times = 3             #reset to 3 "teleports"
    
    delta = 0
    t = 0
    teleport = False

    boostSpeedTime = 5 #powerup lasts 5 seconds
    
    
    #iterator for animation of left and right movement
    leftIterator = 0
    rightIterator = 0

    showFirstBackground = True
    showSecondBackground = False

    TIMER = 100

    leftTimer = 0
    rightTimer = 0
    startTimer = pygame.time.Clock()
    dt = 0
    y=0

 #############################
    start_time = pygame.time.get_ticks()
#############################

    while alive:
        start_time = pygame.time.get_ticks()
        clock = pygame.time.Clock()
    

        #text on the screen
        scoreText = font.render(str("Score: %s" % scoreCount), 1, (255, 0,0)) #update score on screen
        platformText = font.render (str("Platforms left: %s" %(8-len(platformArray))), 1, (0,255,0))
        p_text = font.render(str("Slow-mo: %s" % p_times), 1, (0, 0, 255))
        t_text = font.render(str("Teleports: %s" % t_times), 1, (255, 255, 255))
        slowCountdown = font.render(str ("Time remaining for time slowing: %s" %slowDownTime), 1, (0,255,0) )
        moveSpeedText = font.render(str("Increased movement speed ends in: %s" %boostSpeedTime), 1, (255,255,255))
        
        pygame.event.pump()

        if (showFirstBackground == True):
            screen.blit(background.img, (0,background.loc.y)) #draw beginning background

        if (showSecondBackground == True): 
            screen.blit(background2.img, (0,background2.loc.y)) #this draws second background, if necessary
        screen.blit (scoreText, (0,0))
        screen.blit (platformText, (160, 0))
        screen.blit(p_text, (650, 0))
        screen.blit(t_text, (440, 0))

        hoverImage = pygame.image.load(platformImage) #show the image of platform wherever the player places the mouse
        hoverImage.set_alpha(100)

        screen.blit(hoverImage, (pygame.mouse.get_pos()[0] - 74, pygame.mouse.get_pos()[1]) )

        for evt in pygame.event.get():
            if (evt.type == pygame.QUIT):
                pygame.quit()
                sys.exit()
            if (evt.type == pygame.MOUSEBUTTONDOWN and canStart == True):
                if (evt.button == 1): #1 = left click
                    newPlatform = sprite(pygame.mouse.get_pos()[0] - 74, pygame.mouse.get_pos()[1] , platforms[random.randint(0, len(platforms) - 1)], 0, movingScreenSpeed)
                    if playerObject.imgRect.colliderect(newPlatform.imgRect) == False:
                        
                    #check how many platforms there are.  There can only be 8 platforms on the screen at any given time
                        if (len(platformArray) < 8):
                            if (p_time_bool == True):
                                platformArray.append(sprite(pygame.mouse.get_pos()[0] - 74, pygame.mouse.get_pos()[1] , platforms[random.randint(0, len(platforms) - 1)], 0, movingScreenSpeed) )  
                            else:
                                platformArray.append(sprite(pygame.mouse.get_pos()[0] - 74, pygame.mouse.get_pos()[1] , platforms[random.randint(0, len(platforms) - 1)], 0, movingScreenSpeed) ) 
                            platformCount += 1

                            #random chance to create a falling object for each platform
                            createFallingObject(scoreCount, playerObject)

                elif (evt.button == 2): #2 = middle scroll button
                      if t_times > 0 and teleport == False:
                        target_x, target_y = pygame.mouse.get_pos()
                        #start setting teleportation to player's location
                        teleportation.loc.x, teleportation.loc.y = playerObject.loc.x - 30, playerObject.loc.y - 20
                        teleport = True
                        #set time passed to 0
                        t = 0

                        t_effect.play()
                        teleportation.img = pygame.image.load(teleport_images[0])
                        
            
                elif (evt.button == 3): #3 = right button mouse
                    #ADDED: set up the "slow down" power up
                    if(p_times > 0 and p_time_bool == False and seconds < 0):
                        p_time_bool = True
                        
                        #ADDED: change the variable that holds the speed of the platforms (only way this worked other than hardcoding values)
                        movingScreenSpeed = movingScreenSpeed/2.0

                        for platform in platformArray:
                            platform.v = vector2(0, movingScreenSpeed )  
                        #decrement user powerups
                        p_times -= 1

#ADDED:  Temporary solution, doesn't really work
            if playerObject.current_state == rightJump1:     #if right jump
                playerObject.img = pygame.image.load(rightJump2)
                playerObject.current_state = rightJump2
                
            elif playerObject.current_state == leftJump1:    #if left jump
                playerObject.img = pygame.image.load(leftJump2)
                playerObject.current_state = leftJump2

            #player is in falling motion
            if playerObject.v.y > 0:
                #check direction player is facing in
                #if facing right
                if playerObject.current_state == rightStance or playerObject.current_state == rightJump2:     
                    playerObject.img = pygame.image.load(rightJump1)
                    playerObject.current_state = rightJump1
                elif playerObject.current_state == leftStance or playerObject.current_state == leftJump2:  
                    playerObject.img = pygame.image.load(leftJump1)
                    playerObject.current_state = leftJump1

######
            
            if (evt.type == pygame.KEYDOWN and canStart == True): #make sure you cant move until the timer has ended
                (leftIterator, rightIterator) = playerObject.moveSprite(evt.key, leftIterator, rightIterator)
                dt = startTimer.tick()
            if (evt.type == pygame.KEYUP ): #if key is no longer being pressed
                playerObject.stopMovingSprite(evt.key)
                
        if (playerObject.v.x > 0 or playerObject.v.x < 0 and playerObject.onPlatform == True):
            dt += startTimer.tick()
            if (dt >= 140):
                if(playerObject.current_state == leftStance or playerObject.current_state == leftMoveAnimation[leftIterator]):
                    playerObject.currentState = leftMoveAnimation[leftIterator]
                    playerObject.img = pygame.image.load(leftMoveAnimation[leftIterator])
                    leftIterator = (leftIterator+1) % len(leftMoveAnimation)
                if(playerObject.current_state == rightStance or playerObject.current_state == rightMoveAnimation[rightIterator]):
                    playerObject.currentState = rightMoveAnimation[rightIterator]
                    playerObject.img = pygame.image.load(rightMoveAnimation[rightIterator])
                    rightIterator = (rightIterator+1) % len(rightMoveAnimation)
                dt -= 140


######################TELEPORTATION ANIMATION PROCESS
            
        if teleport == True:
            delta = pygame.time.get_ticks() - start_time
            start_time = pygame.time.get_ticks()
            t += delta
                
            teleportation.loc.x, teleportation.loc.y = playerObject.loc.x - 30, playerObject.loc.y - 20
                

            if t < 60 and t > 30:
                teleportation.img = pygame.image.load(teleport_images[1])
            if t < 90 and t > 60:
               teleportation.img = pygame.image.load(teleport_images[2])
                
            if t < 130 and t > 90:
                #continue animation after first 2 frames have passed
                playerObject.loc.x, playerObject.loc.y = target_x - 30, target_y - 30
                #in case the player teleports more than once while falling, the effects of gravity won't carry over
                playerObject.v.y = 0

                teleportation.img = pygame.image.load(teleport_images[3])
                #set values so you can't jump once you've teleported and you are in mid-air
                playerObject.jump = False
                playerObject.onPlatform = False
            if t < 160 and t > 130:
                teleportation.img = pygame.image.load(teleport_images[4])
#########################


        
        ####################### 
        if teleport == True:
            teleportation.draw(screen)

        #end of teleporting animation
        if t > 160:
            teleport = False
            t_times -= 1
            delta = 0
            t = 0
        ################################  


        playerObject.draw(screen)

        tempSpeedBool = False #used because the following line always overwrites the boolean value here, since this is executed a lot 
    
        (alive, scoreCount, tempSpeedBool) = playerObject.updatePlayer(screen, alive, scoreCount)

        if (tempSpeedBool == True): #this way the variable is only overwritten if actually true
            speedWasBoosted = True
      
        for platform in platformArray: #handles moving the platform
            if (canStart == True):
                platform.updatePlatform(screen)
            else:
                platform.draw(screen)

        #added to move falling objects
        for object in fallingObjectArray:
            object.updateObject(screen)

        y += 1
        background.loc.y+=1
        background2.loc.y+=1


        if (y+HEIGHT == background.imgSize.y): #if the first image in back ends, need to show starting of second image background
            if (showSecondBackground == False):
                showSecondBackground = True
            elif (showFirstBackground == False):
                showFirstBackground = True

        if (y == background.imgSize.y + background2.imgSize.y - HEIGHT): #now background 1 should be shown, above the second one
            showFirstBackground = True
            background.loc.y = -background.imgSize.y

        if (y == background.imgSize.y + background2.imgSize.y): #stop showing second background, only background 1 needs to be shown
            background2.loc.y = -background.imgSize.y - background2.imgSize.y + HEIGHT
            y = 0
            if (showSecondBackground == True):
                showSecondBackground = False
        
        milliseconds += clock.tick_busy_loop(60) #better apparently than clock.tick(60)

        if (seconds >= 0): #show the starting delay timer
            f = pygame.font.Font(None, 75)
            if seconds > 0:
                screen.blit((f.render(str("Begin in: %s" % seconds), 1, (255, 255,255))), (WIDTH/3, HEIGHT/3) )
            elif seconds == 0:
                screen.blit((f.render(str("Start!"), 1, (255, 255,255))), (WIDTH/2.5, HEIGHT/3) )

        if (slowDownTime >= 0 and p_time_bool == True): #show the countdown on the screen for time slowing if it was used
            screen.blit(slowCountdown, (150, 100))
        if (boostSpeedTime >= 0 and speedWasBoosted == True):
            screen.blit(moveSpeedText, (150,150) )

        if milliseconds > 1000:
            milliseconds -= 1000
            if (seconds >= 0): #used for the beginning timer
                seconds -= 1
            if (slowDownTime >= 0 and p_time_bool == True): #decrement the seconds counter for slow time if it was used
                slowDownTime -= 1
            if (boostSpeedTime >= 0 and speedWasBoosted == True): #if the player got a speed boosting powerup
                boostSpeedTime -= 1

        if (seconds <= 0): #beginning timer ended, start moving platforms
            canStart = True

        if (boostSpeedTime < 0):
            movementSpeed = movementSpeedConstant #reset the movement speed back to original value
            boostSpeedTime = 5
            speedWasBoosted = False

        if slowDownTime <= 0: #end of slow down power up time, thus change vel of moving platforms
            slowDownTime = 5
            p_time_bool = False
            movingScreenSpeed = movingScreenCONSTANT
            for platform in platformArray: #back to original speed
                platform.v = vector2(0, movingScreenSpeed)
            
        pygame.display.flip()

    #here begins the loop after the game is over, shows a game over menu, where the user can choose to play again or exit

    playAgain = showGameOverMenu(screen) #show the game over menu function
    pygame.mixer.music.stop()

    if (playAgain == 1): #return value of 1 means the game will continue, thus reset all variables
        alive = True #this allows the inner loop to once again execute
        show = True
        pygame.mixer.music.play(-1)
                       
        #make sure to reset any variables from the game...
        playerObject = sprite(playerStart.x, playerStart.y, rightStance, 0, 0) #reset player variables
        scoreCount = -5 #reset the score

        #delete all platforms from the game now
        platformArray[:] = [] #splices the array or something, removing the items from the array

        #delete the falling objects:
        fallingObjectArray[:] = []

        #starting location for starting platform, where the player will start the game at:
        platformStart = vector2(0, HEIGHT-200 + playerObject.imgSize.y)

        #now create the first platform of the game, so the player can start there:
        platformArray.append(sprite(platformStart.x, platformStart.y, platforms[random.randint(0, len(platforms) - 1)], 0, movingScreenCONSTANT) )

        movingScreenSpeed = movingScreenCONSTANT #used in case the power up is used at the end of game, dying while it is still active

        movementSpeed = movementSpeedConstant

        seconds = 3 #reset the timer when starting the game
        milliseconds = 0
        canStart = False

        platformCount = 0

        #reset the background locations
        background.loc.y = -background.imgSize.y + HEIGHT
        background2.loc.y = -background2.imgSize.y - background.imgSize.y + HEIGHT
