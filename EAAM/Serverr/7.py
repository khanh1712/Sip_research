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

#Read materials
package6 = open("package6.txt", "r")
server = open("Server.txt", "r")

package6Read = package6.readlines()
serverRead = server.readlines()

k3Key = int(package6Read[0][8:])
RCsig = field.Point(curve, field.getPoint(package6Read[1])[0], field.getPoint(package6Read[1])[1])
Ti = field.Point(curve, field.getPoint(package6Read[2])[0], field.getPoint(package6Read[2])[1])
CIDi = int(package6Read[3][7:])
Tf = field.Point(curve, field.getPoint(package6Read[4])[0], field.getPoint(package6Read[4])[1])

groupKey = int(serverRead[3][11:])
s = int(serverRead[1][13:])

#Reconstruct symm key k3
Tsf = s * Tf
x2 = Hash.bytes_to_long(Hash.hash_function(str(Tsf.x)))
Bi = CIDi ^ x2

# Ai_hashed dang sai
# Ai = bytes(a ^ b for (a,b) in zip(Bi, groupKey))
Ai = Bi ^ groupKey
Ai_hashed = Hash.hash_function(str(Ai))

# k3 = bytes(a ^ b for (a,b) in zip(Ai_hashed, x2))
# k3 = Hash.bytes_to_long(k3)

print(Ai)
print(Hash.bytes_to_long(Ai_hashed))


#Verify signature from RC
# if k3 == k3Key:
#     print("true")