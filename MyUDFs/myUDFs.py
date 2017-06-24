

@outputSchema("joinedBag:{t:(type:chararray, n:int, var:int, x:double)}")
def joinBags(b1,b2):
    return b1+b2

@outputSchema("dot:double")
def dot(bag):
    out = 1.0
    for t in bag:
        out = out * t[0]
    return out
