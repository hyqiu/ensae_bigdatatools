import sys
import csv

sys.path.insert(0,'Source/MyFuncs/')

from initArrs import *
from initDirs import *


def printDeltas(deltas,filePath,k):
    deltaS = deltas['deltaS']
    deltaY = deltas['deltaY']
    deltaG = deltas['deltaG']
    printDelta(deltaS,'deltaS',filePath,k)
    printDelta(deltaY,'deltaY',filePath,k)
    printDelta(deltaG,'deltaG',filePath,k)

def printDelta(delta,deltaName,filePath,k):
    f = open(filePath, 'a')
    print>>f,'-----------------------------------------------------'
    print>>f,('Iteration: ' + str(k))
    print>>f,('Delta: ' + deltaName)
    print>>f,'\n'
    print>>f,delta
    print>>f,'\n'

