'''
Eat the orange!
Author : Absera Temesgen
Email: abseratemesgen@gmail.com
June 2020

'''

import pygame
import random
import math
import os

########################   Game Window ###################################

os.environ['SDL_VIDEO_CENTERED'] = '1' # centers the game window
pygame.init()
windowWidth = 900
windowHeight = 600
window = pygame.display.set_mode((windowWidth, windowHeight))
halfWindowWidth = window.get_width()/2
halfWindowHeight = window.get_height()/2
pygame.display.set_caption("Eat the Orange!")
icon = pygame.image.load("images/orange.png")
pygame.display.set_icon(icon)


########################   Classes ###################################


class GameObject:
    ''' Parent class of player and orange.
        object that will be drawn in the window
        drawObject() --> to draw on the screen
        Collisions --> checking presence of collision
    '''
    width, height = 40, 40

    def drawObject(self): 
        croppedImage = pygame.transform.scale(self.image, (self.width, self.height))
        window.blit(croppedImage, (self.xPos, self.yPos))

    def drawAtNewRandomPosition(self):
        self.xPos = random.randint(40, 860)
        self.yPos = random.randint(40, 560)

    def ThereIsACollisionWith(self, otherGameObject):
        x1 = self.xPos
        y1 = self.yPos
        x2 = otherGameObject.xPos
        y2 = otherGameObject.yPos

        distance = math.sqrt(math.pow((x2 - x1), 2) + math.pow((y2 - y1), 2))
        if distance < 27:
            return True
        return False


class Player(GameObject):
    ''' The player controlled by the user '''

    image = pygame.image.load("images/player.png")
    xPos, yPos = 200, 200
    width, height = 40, 40
    velocity = 2

    def showAtCenter(self):
        self.xPos = 380
        self.yPos = 280
        self.width, self.height = 150, 150


class Orange(GameObject):
    ''' The orange that will be eaten by the player. 
        extends methods from GameObject 
    '''
    image = pygame.image.load("images/orange.png")
    xPos, yPos= random.randint(40, 860), random.randint(40, 560)
    width, height = 40, 40


class Enemy(GameObject):
    '''
    There are many enemies in this game.
    because of that they are implemented different from other gameobjects 
    like player and orange.
    '''
    amount = 10
    image = [pygame.image.load("images/enemy.png") for i in range(amount)]
    xPos = [0 for i in range(amount)]
    yPos = [random.randint(0, windowHeight) for i in range(amount)]
    height = [40 for i in range(amount)]
    width = [40 for i in range(amount)]
    velocity = [random.randint(1, 5) for i in range(amount)]

    def draw(self):
        for i in range(self.amount):
            croppedImage = pygame.transform.scale(self.image[i], (self.width[i], self.height[i]))
            window.blit(croppedImage, (self.xPos[i], self.yPos[i]))

    def startMovement(self):
        for i in range(self.amount):
            self.xPos[i] += self.velocity[i]
            if self.xPos[i] >= windowWidth - self.width[i]:
                self.velocity[i] = -self.velocity[i]
            if self.xPos[i] <= 0:
                self.velocity[i] = -self.velocity[i]


    def stopMovement(self):
        for i in range(self.amount):
            self.xPos[i] = -400

    def collideWith(self, otherGameObject):
        x2 = otherGameObject.xPos
        y2 = otherGameObject.yPos
        for i in range(self.amount):
            distance = math.sqrt(math.pow((x2 - self.xPos[i]), 2) + math.pow((y2 - self.yPos[i]), 2))
            if distance < 27:
                return True


class Score:
    '''
    The score will be displayed in the left top corner
    one sccore is added whenever the player eats one orange
    '''
    currentScore = 0
    xPos = 20
    yPos = 2
    fontSize = 30

    def increase(self):
        self.currentScore += 1

    def show(self):
        pygame.font.init()
        myfont = pygame.font.SysFont('Century', self.fontSize)
        textsurface = myfont.render("Score: {0}".format(self.currentScore), False, (0, 0, 0))
        window.blit(textsurface,(self.xPos, self.yPos))

    def ShowAtCenter(self):
        self.xPos = 380
        self.yPos = 220
        self.fontSize = 40


class Life:
    '''
    This is two simple rectangles stacked each other
    when the player collides with the enemy, the width of the upper rectangle decrease
    that reveaes the red rectagle below it
    '''
    currentLife = 5
    xPos = 780
    yPos = 5
    widthGreen = 100
    widthRed = 100
    height = 20

    red = pygame.Color("#ec1c24")
    green = pygame.Color("#0ed145")

    def decrease(self):
        self.widthGreen -= 20 

    def show(self):
        pygame.draw.rect(window, self.red, (self.xPos, self.yPos, self.widthRed, self.height))
        pygame.draw.rect(window, self.green, (self.xPos, self.yPos, self.widthGreen, self.height))

    def thereIsNoLife(self):
        if self.widthGreen <= 0:
            return True
        return False


class Game:
    '''
    This class is the generally the game flow
    '''
    xPos = -1000 # out of the window
    yPos = -1000 # out of the window

    def showGameIntro(self):
        pygame.font.init()
        myfont = pygame.font.SysFont('Century', 30)
        myFontInfo = pygame.font.SysFont('Century', 15)
        textsurface = myfont.render("EAT THE ORANGE", False, color.secondary)
        textSurfaceInfo = myFontInfo.render("Use left, right, up, down keys to move.", False, color.secondary)
        textWidth = textsurface.get_width()
        textHeight = textsurface.get_height()
        window.blit(textsurface,(halfWindowWidth-textWidth/2, halfWindowHeight-textHeight/2-100))
        window.blit(textSurfaceInfo,(halfWindowWidth-textWidth/2, halfWindowHeight-textHeight/2+200))

    def showPlayAgain(self):
        pygame.font.init()
        myfont = pygame.font.SysFont('Century', 30)
        textsurface = myfont.render(f"You scored {score.currentScore}", False, color.secondary)
        textWidth = textsurface.get_width()
        textHeight = textsurface.get_height()
        window.blit(textsurface,(halfWindowWidth-textWidth/2, halfWindowHeight-textHeight/2-100))

    def createGameOver(self):
        pygame.font.init()
        myfont = pygame.font.SysFont('Century', 40)
        textsurface = myfont.render("GAME OVER", False, (0, 0, 0))
        window.blit(textsurface,(self.xPos, self.yPos))

    def showGameOver(self):
        self.xPos = 330
        self.yPos = 170


class Button:
    def __init__(self, c, tc, x, y, w, h, t):
        self.color = c
        self.textColor = tc
        self.xPos = x
        self.yPos = y
        self.width = w
        self.height = h
        self.text = t

    def draw(self):
        pygame.draw.rect(window, self.color, (self.xPos, self.yPos, self.width, self.height), 0)
        font = pygame.font.SysFont('comicsans', 30)
        text = font.render(self.text, 1, self.textColor)
        window.blit(text, (self.xPos + (self.width/2 - text.get_width()/2), self.yPos + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        if pos[0] > self.xPos and pos[0] < self.xPos + self.width:
            if pos[1] > self.yPos and pos[1] < self.yPos + self.height:
                return True

        return False

class CustomColor:
    ''' custom colors '''
    primary = pygame.Color("#d1ccc0")
    secondary = pygame.Color("#ec1c24")


class Sound:
    ''' Sounds that will be heared when some events occur '''

    def playOrangeEaten(self):
        pass
        #TODO: 

    def playEnemyCollide(self):
        pass 
        #TODO:

    def playGameOver(self):
        pass
        #TODO

########################   Loops  ##################################

score = Score()
color = CustomColor()
sound = Sound()
buttonStart = Button(color.secondary, color.primary, halfWindowWidth-100, halfWindowHeight-50, 200, 50, "Start")
buttonPlayAgain = Button(color.secondary, color.primary, halfWindowWidth-100, halfWindowHeight-50, 200, 50, "Play Again")
buttonQuit = Button(color.secondary, color.primary, halfWindowWidth-100,  halfWindowHeight+25, 200, 50, "Quit")
enemy = Enemy()

def gameLoop():
    player = Player()
    orange = Orange()
    game = Game()
    life = Life()
    print("AHSBDAH")

    running = True
    while running:
        pygame.time.delay(3)
        bg = pygame.Color("#d1ccc0")
        window.fill(bg)

        # Key pressed events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    gameIntro()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.xPos > 0:
            player.xPos -= player.velocity
        if keys[pygame.K_RIGHT] and player.xPos < windowWidth - player.width:
            player.xPos += player.velocity
        if keys[pygame.K_UP] and player.yPos > 0:
            player.yPos -= player.velocity
        if keys[pygame.K_DOWN] and player.yPos < windowHeight - player.height:
            player.yPos += player.velocity


        ###### Draws game objects
        player.drawObject()
        orange.drawObject()
        enemy.draw()
        enemy.startMovement()
        score.show()
        life.show()
        game.createGameOver()

        # player collide with the orange
        if player.ThereIsACollisionWith(orange):
            orange.drawAtNewRandomPosition()
            score.increase()
            sound.playOrangeEaten()
            for i in range(enemy.amount):
                enemy.velocity[i] += 0.2

        # player collide with the enemy
        if enemy.collideWith(player):
            player.drawAtNewRandomPosition()
            life.decrease()
            sound.playEnemyCollide()
            if life.thereIsNoLife():
                sound.playGameOver()
                playAgain()
          
        pygame.display.update()  


def playAgain():
    play = True
    while play:
        bg = pygame.Color("#d1ccc0")
        window.fill(bg)
        game = Game()
        game.showPlayAgain()
        buttonPlayAgain.draw()
        buttonQuit.draw()

        # Key pressed events
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                play = False
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if buttonPlayAgain.isOver(pos):
                    score.currentScore = 0
                    play = False
                    gameLoop() # play again
                if buttonQuit.isOver(pos):
                    quit()

            if event.type == pygame.MOUSEMOTION:
                if buttonPlayAgain.isOver(pos):
                    buttonPlayAgain.color = (0, 0, 0)
                else:
                    buttonPlayAgain.color = color.secondary
                    
                if buttonQuit.isOver(pos):
                    buttonQuit.color = (0, 0, 0)
                else:
                    buttonQuit.color = color.secondary

        pygame.display.update()  


def gameIntro():
    intro = True
    while intro:
        window.fill(color.primary)
        game = Game()
        game.showGameIntro()
        buttonStart.draw()
        buttonQuit.draw()

        # Key pressed events
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos() # position of the mouse --> (x, y)

            if event.type == pygame.QUIT:
                intro = False
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if buttonStart.isOver(pos):
                    intro = False
                    gameLoop() # start the game
                if buttonQuit.isOver(pos):
                    quit()

            if event.type == pygame.MOUSEMOTION:
                if buttonStart.isOver(pos):
                    buttonStart.color = (0, 0, 0)
                else:
                    buttonStart.color = color.secondary

                if buttonQuit.isOver(pos):
                    buttonQuit.color = (0, 0, 0)
                else:
                    buttonQuit.color = color.secondary

        pygame.display.update()  


gameIntro()
