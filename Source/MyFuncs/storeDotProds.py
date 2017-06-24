

import sys
import csv

sys.path.insert(0,'Source/MyFuncs/')

from initDirs import *


# store the dot products implemented by pig in the appropriate array
# filePath gives the file where the dot products are stored by pig
# m is the number of historical states (see paper)
# type: 'SS' means that the dotproducts in filePath are <S,S> dotproducts,
#       'YY' means <Y,Y>, 'SY' means <S,Y>, and 'G' means <G,G>, <G,S> and <G,Y>
# arr is the array where we want to store the dot products
# see report for details

def storeDotProds(filePath,m,type,arr):
    f = csv.reader(open(filePath, 'r'), delimiter='\t')
    if type == 'G':
        for l in f:
            i = int(0+1*(l[0]=='S')+2*(l[0]=='Y'))
            j = int(l[3])%m
            arr[i][j] = float(l[4])
    else:
        for l in f:
            i = int(l[1])%m
            j = int(l[3])%m
            arr[i][j] = float(l[4])
    return arr

