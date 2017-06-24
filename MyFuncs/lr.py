
# give the left and right arguments for the script dotProds.pig
# in the case of <S,S> dot products (S = X - previousX, see paper)
def SSLR(SDir,m,i):
    right  = '%s%s%d' % (SDir,'S-',i)
    left = '{'
    for k in range(m):
        left += '%s%s%d' % (SDir,'S-',i-m+1+k)
        if k == m-1:
            left += '}'
        else:
            left += ','
    return [left,right]
    

# same for <Y,Y>
def YYLR(YDir,m,i):
    right  = '%s%s%d' % (YDir,'Y-',i)
    left = '{'
    for k in range(m):
        left += '%s%s%d' % (YDir,'Y-',i-m+1+k)
        if k == m-1:
            left += '}'
        else:
            left += ','
    return [left,right]
    

# same for <S,Y>
def SYLR(SDir,YDir,m,i):
    right1 = '%s%s%d' % (YDir,'Y-',i)
    left1 = '{'
    for k in range(m-1):
        left1 += '%s%s%d' % (SDir,'S-',i-m+1+k)
        if k == m-2:
            left1 += '}'
        else:
            left1 += ','
    left2 = '%s%s%d' % (SDir,'S-',i)
    right2 = '{'
    for k in range(m):
        right2 += '%s%s%d' % (YDir,'Y-',i-m+1+k)
        if k == m-1:
            right2 += '}'
        else:
            right2 += ','
            
    return [left1,right1,left2,right2]
    

# same for <G,G>, <G,S> and <G,Y>
def GLR(GDir,SDir,YDir,i):
    right = '%s%s%d' % (GDir,'G-',i)
    left  = '{'
    left += '%s%s%d' % (GDir,'G-',i)
    left += ','
    left += '%s%s%d' % (SDir,'S-',i)
    left += ','
    left += '%s%s%d' % (YDir,'Y-',i)
    left += '}'
    return [left,right]
    
    

