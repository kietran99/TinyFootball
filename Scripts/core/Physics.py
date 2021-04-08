# import pygame
from collections import namedtuple
import math
from config import *

FRICTION_CO = 8.0

# assume no friction at wall
ENERGY_LOST = 0.3


Vector = namedtuple('Vector', ['x','y'], defaults = [0,0])


def normalizeVector(vector : Vector):
    vectorLength = math.sqrt(vector.x * vector.x + vector.y*vector.y)
    norm = Vector(vector.x / vectorLength, vector.y / vectorLength)
    return norm

def magntude(vector: Vector):
    res = math.sqrt(math.pow(vector.x, 2) + math.pow(vector.y,2))
    # print("value: " + str(res))
    return res

def reflect(inVelo,normVector : Vector):
    # Note that this function only works properly with 4 walls, of which normal vector are (+-1,0) or (0,+-1)
    veloVal = magntude(inVelo)
    veloX = (inVelo.x * normVector.x + inVelo.y * normVector.y)/magntude(normVector)
    if(veloX < 0):
        veloX *= -1
    outVeloVal = math.sqrt(math.pow(veloVal, 2) * (1- ENERGY_LOST))
    # print("Out Velo Value: " + str(outVeloVal) + "\n velo X dir: "+ str(veloX))
    sin = veloX / outVeloVal
    if(sin >= 1):
        sin = 1/sin
    cos = math.sqrt(1 - math.pow(sin, 2))
    subX = (normVector.x * cos + normVector.y * sin)*outVeloVal/magntude(normVector)
    subY = (-normVector.x * sin + normVector.y * cos)*outVeloVal/magntude(normVector)
    if(normVector.x == 0):
        if(inVelo.x * subX > 0):
            subX *= -1
        if(inVelo.y * subY < 0):
            subY *= -1
    if(normVector.y == 0):
        if(inVelo.x * subX < 0):
            subX *= -1
        if(inVelo.y * subY > 0):
            subY *= -1
    return Vector(subX,subY)


    