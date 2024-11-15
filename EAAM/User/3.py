import Hash
import field
from random import randint
from tinyec import registry

samplecurve = registry.get_curve("brainpoolP256r1")
p = samplecurve.field.p
a = samplecurve.a
b = samplecurve.b
x_g = samplecurve.g.x
y_g = samplecurve.g.y
n = samplecurve.field.n
curve = field.Curve(a, b, p, n, x_g, y_g)

# read cert and user info
user = open("User.txt", "r+")
package2 = open("package2.txt", "r")
RC = open("RC.txt", "r")
userRead = user.readlines()
package2Read = package2.readlines()
RCRead = RC.readlines()

# add CA's signature to user info
user.write("\nCA cert: " + package2Read[2])

# Phase 2
i = int(userRead[1][13:])
IDi = int(userRead[0][4:])

Ti = field.Point(curve, field.getPoint(userRead[2])[0], field.getPoint(userRead[2])[1])
Tr = field.Point(curve, field.getPoint(RCRead[2])[0], field.getPoint(RCRead[2])[1])

Fi = Hash.bytes_to_long(Hash.hash_function(str(i) + str(IDi)))
l = randint(pow(2,255), pow(2,256))

Tl = l * curve.g
Tir = i * Tr
Tlr = l * Tr

user.write("\nl = " + str(l))
user.write("\nTlr = " + str(field.displayPoint(Tlr)))

k1 = Hash.bytes_to_long(Hash.hash_function(str(Tir.x) + str(IDi)))
TlrKey = Hash.bytes_to_long(Hash.hash_function(str(Tlr.x)))

# write package 3
package3 = open("package3.txt", "w")
package3.write("TlrKey = " + str(TlrKey) + "\n")
package3.write("k1 = " + str(k1) + "\n")
package3.write("Fi = " + str(Fi) + "\n")
package3.write("Ti = " + str(field.displayPoint(Ti)) + "\n")
package3.write("IDi = " + str(IDi) + "\n")

cert = open("package2.txt", "r")
package3.write(cert.read())
cert.close()
package3.write("\nTl = " + str(field.displayPoint(Tl)) + " ")
package3.close()
package2.close()
RC.close()
user.close()    


