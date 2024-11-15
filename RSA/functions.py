from math import sqrt, ceil
from random import randint

def modulo(coso, somu: int, n):
    # bien so mu thanh binary
    somubin = bin(int(somu))[2:]

    # tinh so du
    mod = 1
    for i in range (len(somubin)):
        mod = ((mod * mod) % n)
        if (somubin[i] == 1):
            mod = ((mod * coso) % n)
    return mod

def isPrime(n):
    if (n <= 11):
        arr =[2,3,5,7,11]
        if (n in arr):
            prime = True
        else:
            prime = False
    else:
        #Find k and q 
        q = n - 1
        k = 0
        while(q % 2 == 0):
            q /= 2
            k += 1
        #Use miller-rabin for 15 times
        for i in range(15):
            prime = False
            base = randint(int(n/2), n-1)
            if (pow(base, int(q), n) == 1):
                prime = True
            else:
                for j in range(k):
                    if (pow(base,int((2**j) * q), n) == n-1):
                        prime = True
                        break

            if (prime == False):
                break
    return prime

def FermatFact(n):
    if(n % 2 == 0):
        return [int(n/2), 2]
    else:
        a = ceil(sqrt(n))
        if (a * a == n):
            return [a,a]
        else:
            while(True):
                b2 = a * a - n
                b = int(sqrt(b2))
                if(b * b == b2):
                    break
                else:
                    a += 1
        return [a - b, a + b]

def isSemiPrime(n):
    # Fermat factorize n
    a = FermatFact(n)[0]
    b = FermatFact(n)[1]
    #check prime of factors
    if (isPrime(a) and isPrime(b)):
        return True
    else:
        return False

# Calculate inverse modulo using extended Euclidean
def inverseMod(d, n):
    t, newt = 0, 1
    r, newr = n, d
    if d < 0:
        return inverseMod(n + d, n)
    else:
        while(newr != 0):
            q = r // newr
            r, newr = newr, (r % newr)
            t, newt = newt, (t - q*newt)
        if r > 1:
            print("not in vertible")
        else:
            if (t < 0):
                t += n
            return int(t)

def millerRabin():
    result = []
    count = 0
    primeLength = int(input("Length of the prime: "))
    while True:
        i = randint(pow(2,primeLength-1), pow(2,primeLength))
        if count == 2:
            break
        if isPrime(i) == True:
            result.append(i)
            count += 1
            print(i, "\n")
    return result        


def keyGen(keyLength: int, p, q):
    phi = (p-1)*(q-1)
    priKey = randint(pow(2,keyLength-1), pow(2,keyLength))
    pubKey = inverseMod(priKey, phi)
    return priKey, pubKey


if __name__ == '__main__':
    prime = millerRabin()
    keyPair = keyGen(64,prime[0], prime[1])
    print(keyPair)