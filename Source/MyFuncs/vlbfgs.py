
import sys
sys.path.insert(0,'Source')

# dot products array are triangular
# convert (i,j) to (min(i,j),max(i,j))
# actually, not so simple... see report for explanations
def convertTriMat(i,j,m,k):
    r  = k-min(k,m-1)
    i1 = (i-r)%m
    j1 = (j-r)%m
    i2 = min(i1,j1)
    j2 = max(i1,j1)
    i3 = (i2+r)%m
    j3 = (j2+r)%m
    return (i3,j3)

# implement deltas (see paper for notation)
# follow the algorithm given in the paper
def vlbfgsDeltas(SSArr,YYArr,SYArr,GArr,m,k):

    mk = min(m,k+1)
    km = k%m

    deltaB = list()
    deltaC = list()
    deltaD = -1.0
    alpha = list()
    for i in range(mk):
        deltaB.append(0.0)
        deltaC.append(0.0)
        alpha.append(0.0)


    for j in range(mk):
        jm = (k-j)%m
        alpha[jm] = 0.0
        for u in range(mk):
            um = (k-u)%m
            c = convertTriMat(um,jm,m,k)
            alpha[jm] += SSArr[c[0]][c[1]] * deltaB[um]
        for u in range(mk):
            um = (k-u)%m
            alpha[jm] += SYArr[jm][um] * deltaC[um]
            ### alpha[jm] += SYArr[um][jm] * deltaC[um]
        alpha[jm] += GArr[1][jm] * deltaD
        alpha[jm] /= SYArr[jm][jm]
        deltaC[jm] -= alpha[jm]

    for i in range(mk):
        deltaB[i] *= SYArr[km][km] / YYArr[km][km]
        deltaC[i] *= SYArr[km][km] / YYArr[km][km]
    deltaD *= SYArr[km][km] / YYArr[km][km]
    
    for i in range(mk):
        j = mk-1-i
        jm = (k-j)%m
        beta = 0
        for u in range(mk):
            um = (k-u)%m
            beta += SYArr[um][jm] * deltaB[um]
            ### beta += SYArr[jm][um] * deltaB[um]
        for u in range(mk):
            um = (k-u)%m
            c = convertTriMat(um,jm,m,k)
            beta += YYArr[c[0]][c[1]] * deltaC[um]
        beta += GArr[2][jm] * deltaD
        beta /= SYArr[jm][jm]
        deltaB[jm] += alpha[jm] - beta

    return {'deltaS': deltaB, 'deltaY':deltaC, 'deltaG':deltaD}

