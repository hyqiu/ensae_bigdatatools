
# initialize the arrays for <S,S>, <Y,Y>, ...
def initArrs(nrow,nrowG,ncol):
    SSArr = initArr(nrow,ncol)
    YYArr = initArr(nrow,ncol)
    SYArr = initArr(nrow,ncol)
    GArr  = initArr(nrowG,ncol)
    return [SSArr,YYArr,SYArr,GArr]

# initialise an array with nrow and ncol
def initArr(nrow,ncol):
    r = list()
    for i in range(nrow):
        inner = list()
        for j in range(ncol):
            inner.append(0.0)
        r.append(inner)
    return r
