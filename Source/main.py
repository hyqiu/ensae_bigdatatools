
#######################################################################################
### OBJECTIVE
#######################################################################################

## Large-scale VL-BFGS using MapReduce
## Given a function f(X) with an unique minimum
## We want to find X = argmin f(X)

#######################################################################################
### LIBRARY
#######################################################################################


import sys

sys.path.insert(0,'Source/MyUDFs/')
sys.path.insert(0,'Source/MyFuncs/')

from org.apache.pig.scripting import Pig

from initDirs import *
from initArrs import *
from lr import *
from storeDotProds import *
from vlbfgs import *
from runPigScripts import *

sys.path.insert(0,'Source/Debug/')               #FOR DEBUGGING
from printArr import *                           #FOR DEBUGGING
from printDelta import *                         #FOR DEBUGGING


#######################################################################################
### PARAMETERS
#######################################################################################

# number of historical states to use
m = 5

# length of the variable to optimize
nvar = 5

# number of iterations
k = 100

# alpha should be determined by the Wolfe conditions
# not implemented yet
# we take an arbitrary value for alpha
alpha = 0.1


#######################################################################################
### DIRECTORIES
#######################################################################################

# all the scripts are in the Source/ folder
sourceDir = 'Source/'

# all data are in the Data/ folder
dataDir   = 'Data/'

#dataSaveDir = 'DataSave/' # To delete

# folders for X, S, G, and Y (see the paper for notation)
XDir        = dataDir    + 'X/'
SDir        = dataDir    + 'S/'
GDir        = dataDir    + 'G/'
YDir        = dataDir    + 'Y/'

# all elements in TmpDir are temporary
TmpDir      = dataDir    + 'Tmp/'

# store dot products produced by pig and required by python
dotProdDir  = TmpDir     + 'DotProd/'

# store arrays of dot products
arrDir      = TmpDir     + 'Arr/'

# store deltas (see the paper for notation)
deltaDir    = TmpDir     + 'Delta/'

# store dot products produced by pig and required by python
dotProdFile = dotProdDir + 'part-r-00000'

# store deltas (see the paper for notation)
deltaFile   = deltaDir   + 'delta'

# for debugging only
arrLog      = arrDir     + 'arrLog'            #FOR DEBUGGING
deltaLog    = deltaDir   + 'deltaLog'          #FOR DEBUGGING


#######################################################################################
### SCRIPTS
#######################################################################################


gradientPigScript  = sourceDir + 'Pigs/gradient.pig'
dotProdsPigScript  = sourceDir + 'Pigs/dotProds.pig'
updateXnSPigScript = sourceDir + 'Pigs/updateXnS.pig'


#######################################################################################
### INIT
#######################################################################################


initDirs(dataDir,m,nvar)
SSArr,YYArr,SYArr,GArr = initArrs(m,3,m)


#######################################################################################
### MAIN LOOP
#######################################################################################


for i in range(k):
    
    # see Source/MyFuncs/runPigScripts.py
    runGradient(gradientPigScript,XDir,GDir,YDir,i)
    
    # see Source/MyFuncs/lr.py
    left , right = SSLR(SDir,m,i)
    # see Source/MyFuncs/runPigScripts.py
    runDotProds(dotProdsPigScript,left,right,dotProdDir)
    print('\n\n\n\n\n\n\n\n')
    # see Source/MyFuncs/storeDotProds.py
    SSArr = storeDotProds(dotProdFile,m,'SS',SSArr)

    # see Source/MyFuncs/lr.py
    left , right = YYLR(YDir,m,i)
    # see Source/MyFuncs/runPigScripts.py
    runDotProds(dotProdsPigScript,left,right,dotProdDir)
    # see Source/MyFuncs/storeDotProds.py
    YYArr = storeDotProds(dotProdFile,m,'YY',YYArr)

    # see Source/MyFuncs/lr.py
    left1 , right1, left2, right2 = SYLR(SDir,YDir,m,i)
    # see Source/MyFuncs/runPigScripts.py
    runDotProds(dotProdsPigScript,left1,right1,dotProdDir)
    # see Source/MyFuncs/storeDotProds.py
    SYArr = storeDotProds(dotProdFile,m,'SY',SYArr)
    # see Source/MyFuncs/runPigScripts.py
    runDotProds(dotProdsPigScript,left2,right2,dotProdDir)
    # see Source/MyFuncs/storeDotProds.py
    SYArr = storeDotProds(dotProdFile,m,'SY',SYArr)

    # see Source/MyFuncs/lr.py
    left , right = GLR(GDir,SDir,YDir,i)
    # see Source/MyFuncs/runPigScripts.py
    runDotProds(dotProdsPigScript,left,right,dotProdDir)
    # see Source/MyFuncs/storeDotProds.py
    GArr = storeDotProds(dotProdFile,m,'G',GArr)

    # for debugging: print arrays SSArr, YYArr, SYArr and GArr in a txt file
    printArrs(SSArr, YYArr, SYArr, GArr, arrLog,i)               #FOR DEBUGGING

    # see Source/MyFuncs/vlbfgs.py
    deltas = vlbfgsDeltas(SSArr,YYArr,SYArr,GArr,m,i)

    # for debugging: print deltas in a txt file
    printDeltas(deltas,deltaLog,i)                               #FOR DEBUGGING

    # see Source/MyFuncs/runPigScripts.py
    runUpdateXnS(updateXnSPigScript,deltas,deltaFile,m,i,alpha)

#######################################################################################

