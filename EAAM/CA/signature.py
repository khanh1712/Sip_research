import field
import Hash
import secrets
from tinyec import registry

samplecurve = registry.get_curve("brainpoolP256r1")
p = samplecurve.field.p
a = samplecurve.a
b = samplecurve.b
x_g = samplecurve.g.x
y_g = samplecurve.g.y
n = samplecurve.field.n
curve = field.Curve(a, b, p, n, x_g, y_g)

def ECC_sign(message, priKey): 
    # hash then sign
    h = Hash.bytes_to_long(Hash.hash_function(message))
    # r and s are 2 components of the signature
    r = 0
    s = 0
    while r == 0:
        # generate a random k 
        k = secrets.randbelow(n)
        point = k * curve.g
        r = point.x % n
    while s == 0:
        s = field.inverseMod(k, n) * (h + r * priKey) % n
    
    # f = open("cert.txt", "w")
    # f.write(str(r) + "\n" + str(s))
    # f.close()
    return (r, s)


def ECC_verify_sign(message, signature, pubKey):
    h = Hash.bytes_to_long(Hash.hash_function(message))
    u1 = field.inverseMod(signature[1], n) * h % n
    u2 = field.inverseMod(signature[1], n) * signature[0] % n

    point = u1 * curve.g + u2 * pubKey

    if (point.x - signature[0]) % n == 0:
        return True
    return False
