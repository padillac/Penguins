# Python re-creation of "Knockout" by GamePigeon
#Chris Padilla
#Date/Time: 5/29 10:00am

#Current State: Movement and collisions are functional, need to fix angles of collisions which are sometimes erratic. Also need to fix glitch where penguins get stuck on top of each other and infinitely collide. Also need to make setup.py modify the Queue size in mttkinter.py once installed to avoid queue.Full errors.


import sys
#Allow local imports
sys.path.insert(1, 'Classes/')
sys.path.insert(1, 'Libraries/')


import mttkinter
from graphics import *
from random import *
from threading import *
from time import sleep
from math import *
from PenguinClass import *
from PlayerClass import *

#creates game window and initial iceberg
def createGameWindow():
    GW = GraphWin("Penguins", 1100, 750)
    GW.setCoords(-12,-12,12,12)
    GW.setBackground(color_rgb(160,210,255))

    iceberg = Rectangle(Point(-10,-10), Point(10,10))
    iceberg.setFill("white")
    iceberg.setOutline("grey")
    iceberg.draw(GW)

    return GW, iceberg

#function to initialize a new game
def beginGame(GW, p1, p2):

    allPenguins = []
    for player in [p1, p2]:
        for i in range(4):
            x = randint(-9,9)
            y = randint(-9,9)
            newP = Penguin(x,y,player,GW)
            allPenguins.append(newP)
            #this loop tries to eliminate collisions when penguins are first created.
            #NEEDS TO BE FIXED TO CATCH COLLISIONS AS A RESULT OF BEING MOVED INTO OTHER NEARBY PENGUINS.
            for p in allPenguins:
                if newP != p:
                    while newP.isCollision(p):
                        newP.tpmove([uniform(-2,2), uniform(-2,2)])

    for p in allPenguins:
        p.appear()
        p.setAllPenguins(allPenguins)

    return allPenguins


def takeFullTurn(GW, iceberg, allPenguins, player1, player2):
    #creates dictionary of penguin objects and movement vectors for the player object called
    print("getting player 1's moves")
    p1NextMoves = player1.takeTurn(GW, allPenguins)
    #gets player 2's moves -- switch to network version somehow
    print("getting player 2's moves")
    p2NextMoves = player2.takeTurn(GW, allPenguins)

    #start all collision checkers, clearing "last penguin hit"
    for i in allPenguins:
        i.endCollisionChecker()
        Thread(target = i.startCollisionChecker, args = (i, iceberg,)).start()


    #runs each chosen move command in a separate thread
    for p in p1NextMoves.keys():
        Thread(target = p.move, args = (p1NextMoves[p], iceberg,)).start()
    for p in p2NextMoves.keys():
        Thread(target = p.move, args = (p2NextMoves[p], iceberg,)).start()



#main module/code testing
def main():
    #initialization
    GW, iceberg = createGameWindow()
    player1 = Player("black")
    player2 = Player("blue")
    allPenguins = beginGame(GW, player1, player2)

    gameOver = False

    time.sleep(1)


    #set up "while game not over" loop that repeats full turns and iceberg shrinking?
    while not gameOver:
        takeFullTurn(GW, iceberg, allPenguins, player1, player2)
        #check game ending conditions:
        if player1.getLivePenguinsNum() == 0 or player2.getLivePenguinsNum() == 0:
            gameOver = True

        #shrink iceberg

    print("GAME OVER")



    #end stuff
    GW.getMouse()
    GW.close()

if __name__ == "__main__":
    main()
