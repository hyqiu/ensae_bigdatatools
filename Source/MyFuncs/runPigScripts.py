import sys
sys.path.insert(0,'Source/MyFuncs/')
from initDirs import rmDotProdTmp

from org.apache.pig.scripting import Pig

def runPigScript(pigScript,params):
    P = Pig.compileFromFile(pigScript)
    bound = P.bind(params)
    stat=bound.runSingle()

# see gradient.pig
def runGradient(pigScript,XDir,GDir,YDir,n):
    params = {'XInput'  : '%s%s%d' % (XDir,'X-',n),
              'GInput'  : '%s%s%d' % (GDir,'G-',n-1),
              'GOutput' : '%s%s%d' % (GDir,'G-',n),
              'YOutput' : '%s%s%d' % (YDir,'Y-',n)}
    runPigScript(pigScript,params)

# see dotProds.pig
def runDotProds(pigScript,left,right,out):
    rmDotProdTmp(out)
    params = {'left' : left,
              'right': right,
              'out'  : out}
    runPigScript(pigScript,params)


# Implement the new value of X (see paper)
# we also update S <- X - previousX
# see updateXnS.pig
def runUpdateXnS(pigScript,deltas,deltasFile,m,k,alpha):
    
    deltaS = deltas['deltaS']
    deltaY = deltas['deltaY']
    deltaG = deltas['deltaG']
    
    for i in range(max(0,m-len(deltaS))):
        deltaS.append(0.0)
    for i in range(max(0,m-len(deltaY))):
        deltaY.append(0.0)

    file = open(deltasFile,'w')
    for  i in range(len(deltaS)):
        file.write('S\t')
        file.write(str(k-i))
        file.write('\t')
        file.write(str(deltaS[i]))
        file.write('\n')
    for  i in range(len(deltaY)):
        file.write('Y\t')
        file.write(str(k-i))
        file.write('\t')
        file.write(str(deltaY[i]))
        file.write('\n')
    file.write('G\t')
    file.write(str(k))
    file.write('\t')
    file.write(str(deltaG))
    file.close()

    Input = '{'
    for i in range(k-m+1,k+1):
        Input = Input + 'Data/S/S-' + str(i) + ','
    for i in range(k-m+1,k):
        Input = Input + 'Data/Y/Y-' + str(i) + ','
    Input = Input + 'Data/G/G-' + str(k) + '}'

    params = {'deltasFile': deltasFile,
              'n'         : k+1,
              'alpha'     : alpha,
              'Input'     : Input,
              'XInput'    : 'Data/X/X-' + str(k),
              'SOutput'   : 'Data/S/S-' + str(k+1),
              'XOutput'   : 'Data/X/X-' + str(k+1)}

    runPigScript(pigScript,params)
