import field
from tinyec import registry
from time import time
import random

samplecurve = registry.get_curve("brainpoolP512r1")
p = samplecurve.field.p
a = samplecurve.a
b = samplecurve.b
x_g = samplecurve.g.x
y_g = samplecurve.g.y
n = samplecurve.field.n
curve = field.Curve(a, b, p, n, x_g, y_g)


def keyGen(keyLength: int):
    priKey = random.randint(pow(2,keyLength-1), pow(2,keyLength))
    pubKey = priKey*curve.g
    return priKey, pubKey


count = 1000
sum = 0

for i in range(count):
    start = time()
    k = keyGen(256)
    end = time()
    runtime = end - start
    sum += runtime

avg = sum / count
print("\nRuntime: ", avg)

