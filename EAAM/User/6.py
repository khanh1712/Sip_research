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

#Read user materials
user = open("User.txt", "r")
server = open("Server.txt", "r")

userRead = user.readlines()
serverRead = server.readlines()

i = int(userRead[1][13:])
Ti = field.Point(curve, field.getPoint(userRead[2])[0], field.getPoint(userRead[2])[1])
IDi = int(userRead[0][4:])
Bi = int(userRead[6][5:])
Ci = int(userRead[7][5:])
RCsig = field.Point(curve, field.getPoint(userRead[8])[0], field.getPoint(userRead[8])[1])
Ts = field.Point(curve, field.getPoint(serverRead[2])[0], field.getPoint(serverRead[2])[1])

#Cooking
Fi = Hash.bytes_to_long(Hash.hash_function(str(i) + str(IDi)))
f = randint(pow(2,255), pow(2,256))
Tf = f * curve.g
Tfs = f * Ts

x1 = Hash.hash_function(str(Fi) + str(Ti) + str(IDi))
x2 = Hash.hash_function(str(Tfs.x))

Bi = Hash.long_to_bytes(Bi)
Ci = Hash.long_to_bytes(Ci)

Ai_hashed = bytes(a ^ b for (a,b) in zip(Ci, x1))
CIDi = bytes(a ^ b for (a,b) in zip(Bi, x2))
k3Key = bytes(a ^ b for (a,b) in zip(Ai_hashed, x2))

#write package 6

package6 = open("package6.txt", "w")
package6.write("k3Key = " + str(Hash.bytes_to_long(k3Key)) + "\n")
package6.write("RCsig = " + str(field.displayPoint(RCsig)) + "\n")
package6.write("Ti = " + str(field.displayPoint(Ti)) + "\n")
package6.write("CIDi = " + str(Hash.bytes_to_long(CIDi)) + "\n")
package6.write("Tf = " + str(field.displayPoint(Tf)) + " ")


print(Hash.bytes_to_long(Ai_hashed))

package6.close()
user.close()
server.close()