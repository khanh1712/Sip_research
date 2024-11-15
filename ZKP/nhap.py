def gcd(a,b):
    if(a>b):
        r1=a
        r2=b
    else:
        r1=b
        r2=a
    while(r2>0):
        q=int(r1/r2)
        r=(r1-q*r2)
        r1=r2
        r2=r

    return(r1)

print(gcd(2740,1760))
print(gcd(1760,2740))