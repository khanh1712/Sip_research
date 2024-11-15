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

user = open("User.txt", "r+")
id = user.read()[4:9]
# init User: choose gen private key and public key
priKey = randint(pow(2,255), pow(2,256))
pubKey = priKey*curve.g

user.write("\nPrivate key: " + str(priKey) + "\nPublic key: " + str(field.displayPoint(pubKey)))
user.close()

# creat package 1: id and public key
f = open("package1.txt", "w")
f.write( "ID: " + str(id) + "\nPublic key: " + str(field.displayPoint(pubKey)))
f.close()
