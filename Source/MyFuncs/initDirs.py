
import random
import commands

# function called by initDirs()
# initialise the starting points for X, Y, S, G
# sometimes it is 0 (for G for example)
# sometimes it is a random value (for X for example)
def init(umin,umax,d,t,n,nvar):
    shellCMD = 'mkdir ' + d + t + '-' + str(n) + '/'
    commands.getstatusoutput(shellCMD)
    f = open(d + t + '-' + str(n) + '/part-r-00000','w')
    for i in range(nvar):
        f.write(t+'\t')
        f.write(str(n)+'\t')
        f.write(str(i)+'\t')
        f.write(str(random.uniform(umin,umax))+'\n')
    

# initialise all the folders we need
# see report for details
def initDirs(dataDir,m,nvar):
    commands.getstatusoutput('mkdir ' + dataDir)
    commands.getstatusoutput('cd ' + dataDir + '; mkdir Tmp; cd ..')
    commands.getstatusoutput('cd ' + dataDir + '/Tmp; mkdir Arr Delta; cd ../..')
    commands.getstatusoutput('cd ' + dataDir + '; mkdir Tmp; cd Tmp; mkdir DotProd Arr Delta;' + 'cd ..')
    commands.getstatusoutput('cd ' + dataDir + '; mkdir ' + 'X G S Y;' + 'cd ..')
    init(-10,10,dataDir + 'X/','X',0,nvar)
    init(-10,10,dataDir + 'S/','S',0,nvar)
    init(0,0,dataDir + 'G/', 'G', -1, nvar)
    for i in range(m):
        init(0,0,dataDir + 'Y/', 'Y', -1-i, nvar)
    for i in range(m):
        init(0,0,dataDir + 'S/', 'S', -1-i, nvar)


#def initDirs(dataSaveDir,dataDir):
#    shellCMD = 'rm -rf ' + dataDir
#    commands.getstatusoutput(shellCMD)
#    shellCMD = 'cp -rf ' + dataSaveDir + ' ' + dataDir
#    commands.getstatusoutput(shellCMD)


# dotProdTmp is where the dotproducts pig is implementing is stored
# one these dotproducts are stored by python in the appropriate arrays: SSArr, YYArr...
# then we remonve dotProdTmp with this function because pig cannot overwrite it
def rmDotProdTmp(dotProdTmp):
    shellCMD = 'rm -rf ' + dotProdTmp
    commands.getstatusoutput(shellCMD)
