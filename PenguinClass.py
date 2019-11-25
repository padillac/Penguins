import mttkinter #add try/catch block which will automatically install package if import fails??
from graphics import *
from random import *
from threading import *
from time import sleep
from math import *

#Penguin Object Class
class Penguin:

    def __init__(self, x, y, player, window):
        self.allPenguins = []
        self.pos = Point(x,y)
        self.player = player
        self.team = player.team
        self.window = window
        self.sprite = Circle(self.pos, 1)
        self.sprite.setFill(self.team)
        self.isAlive = True
        self.vector = [0,0]
        self.CollisionVector = [0,0]
        self.collision = False
        self.collidesWith = self
        self.StopCollisionThread = False


    #initialize allPenguins variable
    def setAllPenguins(self, allPenguins):
        self.allPenguins = allPenguins
    #returns the team that the penguin is on
    def getTeam(self):
        return self.team
    #returns position point to allow for collision checking.
    def getPos(self):
        return self.pos
    #returns current vector of penguin for momentum equations
    def getVector(self):
        return self.CollisionVector
    #makes penguin's sprite appear. possibly move this to __init__ ??
    def appear(self):
        self.sprite.draw(self.window)

    #kills the penguin, updating player attributes
    def kill(self):
        self.isAlive = False
        self.endCollisionChecker()
        self.player.livePenguinsNum -= 1
        self.sprite.undraw()

    def isCollision(self, p2):
        checkD = 2
        p1 = self.pos
        try:
            p2 = p2.pos
        except AttributeError:
            p2 = p2
            checkD = 1
        distance = sqrt((p1.getX() - p2.getX())**2 + (p1.getY() - p2.getY())**2)
        if distance <= checkD:
            return True
        return False

    def computeCollisionVector(self, v1, v2, p2pos):
        p1x = self.pos.getX()
        p1y = self.pos.getY()
        p2x = p2pos.getX()
        p2y = p2pos.getY()
        v1s = sqrt(v1[0]**2 + v1[1]**2)
        v2s = sqrt(v2[0]**2 + v2[1]**2)
        v1x = v1[0]
        v1y = v1[1]
        v2x = v2[0]
        v2y = v2[1]
        try:
            v1Angle = atan2(v1y, v1x)
        except ZeroDivisionError:
            v1Angle = 0
        try:
            v2Angle = atan2(v2y, v2x)
        except ZeroDivisionError:
            v2Angle = 0

        #FIGURE OUT WHAT THE HECK THIS ANGLE CALCULATION IS
        #cAngle = atan2((p2y - p1y), (p2x - p1x)) # <- wrong angle???
        #cAngle = abs(v1Angle) - abs(v2Angle)
        cAngle = v1Angle - v2Angle


        #momentum equations to calculate new vector components
        #NEED TO FIX SO THAT ANGLES ARE ALWAYS RIGHT
        newX = (v1s * cos(v1Angle - cAngle)*(1 - 1) + (2 * v2s * cos(v2Angle - cAngle)))*(cos(cAngle))/(2) + v1s*sin(v1Angle - cAngle)*sin(cAngle)
        newY = (v1s * cos(v1Angle - cAngle)*(1 - 1) + (2 * v2s * cos(v2Angle - cAngle)))*(sin(cAngle))/(2) + v1s*sin(v1Angle - cAngle)*cos(cAngle)

        #uncomment line below for collision vector info for troubleshooting
        #print("collision with vectors:", v1, "and", v2, "new vector:", [newX,newY])
        return [newX, newY]

    #Function to run in a separate thread and monitor for collisions
    def CollisionChecker(self, lastP, iceberg):
        while not self.StopCollisionThread:
            time.sleep(.000000000000000000000001) #This number can be tweaked to improve performance
            for p2 in self.allPenguins:
                if p2 != self and p2 != lastP: #lastP variable is so that two penguins don't keep colliding with each other indefinitely. If collision mechanics can be fixed, maybe this functionality won't be necessasry
                    if self.isCollision(p2):
                        #print("COLLISION:", self.toString(), p2.toString())
                        self.collision = True
                        self.collidesWith = p2
                        self.CollisionVector = self.vector
                        time.sleep(.00000000000000000000001)
                        p2Vector = self.collidesWith.getVector()
                        p2Center = self.collidesWith.pos
                        newVector = self.computeCollisionVector(self.CollisionVector, p2Vector, p2Center)
                        time.sleep(.00000000000000000000001)

                        Thread(target = self.move, args = (newVector, iceberg)).start()
                        self.CollisionVector = [0,0]
                        self.endCollisionChecker()
        #once function has exited, start it again, unless penguin is dead
        if self.isAlive:
            self.startCollisionChecker(self.collidesWith, iceberg)

    def startCollisionChecker(self, lastP, iceberg):
        #Collision checker thread
        self.StopCollisionThread = False
        CollisionCheckerProcess = Thread(target = self.CollisionChecker, args = (lastP, iceberg,), daemon = True)
        CollisionCheckerProcess.start()

    def endCollisionChecker(self):
        self.StopCollisionThread = True

    #function that immediately teleports a penguin for administration purposes.
    def tpmove(self, vec):
        self.sprite.move(vec[0], vec[1])
        self.pos = self.sprite.getCenter()

    #function that moves a penguin along a directional vector, and implements collisions and death-checking
    def move(self, dirvec, iceberg):
        self.collision = False
        #creates a line to view the directional vector
        arrow = Line(self.pos, Point(self.pos.getX() + dirvec[0], self.pos.getY() + dirvec[1]))
        arrow.draw(self.window)

        #sets penguins vector variable to the inputted directional vector.
        self.vector = dirvec

        def moveSprite():
            def checkOutOfBounds():
                lowX = iceberg.getP1().getX()
                highX = iceberg.getP2().getX()
                lowY = iceberg.getP1().getX()
                highY = iceberg.getP2().getY()
                if self.pos.getX() < lowX or self.pos.getX() > highX:
                    return True
                if self.pos.getY() < lowY or self.pos.getY() > highY:
                    return True
                return False
            #central loop that moves the penguin at a decaying rate.
            while ((abs(self.vector[0]) > 0.1 or abs(self.vector[1]) > 0.1) and not self.collision and self.isAlive):
                dx, dy = self.vector[0]/100, self.vector[1]/100
                self.sprite.move(dx, dy)
                self.pos = self.sprite.getCenter()
                #check if penguin is dead
                if checkOutOfBounds():
                    self.kill()
                self.vector[0] = self.vector[0]*(.99)
                self.vector[1] = self.vector[1]*(.99)
                time.sleep(10**-500) #This number can be tweaked to improve performance

        #movesprite thread
        moveSpriteProcess = Thread(target = moveSprite)
        moveSpriteProcess.start()

        #starts the collision checker if it is currently off.
        #def restartCollisionChecker():
            #time.sleep(.01)
        #    self.startCollisionChecker()
        #if self.StopCollisionThread: #if a collision has just occurred
        #    Thread(target = restartCollisionChecker).start()


    def getPenguinMoveVector(self):
        point1 = self.pos
        point2 = self.window.getMouse()
        newMoveVector = [point2.getX() - point1.getX(), point2.getY() - point1.getY()]
        #visual representation of new movement vector
        newMoveLine = Line(point1, point2)
        newMoveLine.setFill("red")
        newMoveLine.draw(self.window)
        #return the new vector to allow new movement
        return newMoveVector





    def toString(self):
        return "Penguin Object @{}".format(self.pos)
