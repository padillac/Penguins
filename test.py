from graphics import *
from random import *
from threading import *
from time import sleep
from math import *


"""
def test1():
    for i in range(30):
        print("A", i)
        time.sleep(.01)

def test2():
    for i in range(30):
        print("B", i)
        time.sleep(.01)

def test3():
    for i in range(30):
        print("C", i)
        time.sleep(.01)

t1 = Thread(target = test1)
t2 = Thread(target = test2)
t3 = Thread(target = test3)

t1.start()
t2.start()

"""


"""
def timer():
    time.sleep(6)
    print("TIMER DONE")

def tester():
    print("tester started")
    print(type(t))
    print(t.is_alive())
    if t.is_alive():
        print("t.is_alive()")

t = Thread(target = timer)

t2 = multiprocessing.Process(target = tester)

t3 = multiprocessing.Process(target = tester)


if __name__ == "__main__":
    t.start()
    print("t started")
    time.sleep(1)

    t2.start()
    print("t2 started")
    time.sleep(2)
    print(t.is_alive())
        time.sleep(2)
    print("terminating t")
    t.terminate()
"""


v2 = [-2.5184733854476162, -1.888855039085713]
v1 = [0, 0]
#new vector: [2.543658119302093, 2.694766522428951]
"""
v1 = [-2.8332825586285684, 2.8332825586285684]
v2 = [-2.5184733854476162, -1.888855039085713]
#new vector: [2.594027587011047, -1.8384855713767612]
"""
def computeCollisionVector(v1, v2):
    #p1x = self.pos.getX()
    #p1y = self.pos.getY()
    #p2x = p2pos.getX()
    #p2y = p2pos.getY()
    v1s = sqrt(v1[0]**2 + v1[1]**2)
    v2s = sqrt(v2[0]**2 + v2[1]**2)
    v1x = v1[0]
    print("v1x",v1x)
    v1y = v1[1]
    print("v1y",v1y)
    v2x = v2[0]
    print("v2x",v2x)
    v2y = v2[1]
    print("v2y",v2y)
    try:
        v1Angle = atan2(v1y, v1x)
    except ZeroDivisionError:
        v1Angle = 0
    print("v1Angle",v1Angle)
    try:
        v2Angle = atan2(v2y, v2x)

    except ZeroDivisionError:
        v2Angle = 3*pi/2
    print("v2Angle",v2Angle)

    #cAngle = atan2((p2y - p1y), (p2x - p1x)) # <- wrong angle???
    cAngle = v2Angle - v1Angle
    print("cAngle",cAngle)

    #momentum equations to calculate new vector components
    #NEED TO FIX SO THAT ANGLES ARE ALWAYS RIGHT
    newX = (v1s * cos(v1Angle - cAngle)*(1 - 1) + (2 * v2s * cos(v2Angle - cAngle)))*(cos(cAngle))/(2) + v1s*sin(v1Angle - cAngle)*sin(cAngle)
    print("newX",newX)
    newY = (v1s * cos(v1Angle - cAngle)*(1 - 1) + (2 * v2s * cos(v2Angle - cAngle)))*(sin(cAngle))/(2) + v1s*sin(v1Angle - cAngle)*cos(cAngle)
    print("newY",newY)

    print("collision with vectors:", v1, "and", v2, "new vector:", [newX,newY])

computeCollisionVector(v1,v2)
