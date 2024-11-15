import field
import Hash
from tinyec import registry

samplecurve = registry.get_curve("brainpoolP256r1")
p = samplecurve.field.p
a = samplecurve.a
b = samplecurve.b
x_g = samplecurve.g.x
y_g = samplecurve.g.y
n = samplecurve.field.n

curve = field.Curve(a, b, p, n, x_g, y_g)

# open package
package4 = open("package4.txt", "r")
server = open("Server.txt", "r")
user = open("User.txt", "r+")

package4Read = package4.readlines()
serverRead = server.readlines()
userRead = user.readlines()

# Extract info
Tlr = field.Point(curve, field.getPoint(userRead[5])[0], field.getPoint(userRead[5])[1])
IDi = int(userRead[0][4:])
k2 = int(package4Read[0][5:])
k2Key = Hash.bytes_to_long(Hash.hash_function(str(Tlr.x) + str(IDi)))

if k2 == k2Key:
    Bi = int(package4Read[1][5:])
    Ci = int(package4Read[2][5:])
    sigRC = (field.getPoint(package4Read[3])[0], field.getPoint(package4Read[3])[1])

    user.write("\n"+ package4Read[1] + package4Read[2] + package4Read[3])

else:
    print("Not legit RC")

