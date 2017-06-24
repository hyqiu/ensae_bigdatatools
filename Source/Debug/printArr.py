


import sys
import csv

sys.path.insert(0,'Source/MyFuncs/')

from initArrs import *
from initDirs import *


#m = 5
#SSArr,YYArr,SYArr,GArr = initArrs(m,3,m)

#filePath = 'Data/Arr/Tmp/arr'

def printArrs(SSArr,YYArr,SYArr,GArr,filePath,k):
    printArr(SSArr,'SSArr',filePath,k)
    printArr(YYArr,'YYArr',filePath,k)
    printArr(SYArr,'SYArr',filePath,k)
    printArr(GArr,'GArr',filePath,k)

def printArr(arr,arrName,filePath,k):
    f = open(filePath, 'a')
    print>>f,'-----------------------------------------------------'
    print>>f,('Iteration: ' + str(k))
    print>>f,('Arr: ' + arrName)
    print>>f,'\n'
    for i in arr:
        print>>f, i
    print>>f,'\n'

#printArrs(filePath,3)

