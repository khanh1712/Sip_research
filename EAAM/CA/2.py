import signature
import field
from tinyec import registry
from random import randint

samplecurve = registry.get_curve("brainpoolP256r1")
p = samplecurve.field.p
a = samplecurve.a
b = samplecurve.b
x_g = samplecurve.g.x
y_g = samplecurve.g.y
n = samplecurve.field.n

curve = field.Curve(a, b, p, n, x_g, y_g)
priKeyCA = randint(pow(2,255), pow(2,256))
pubKeyCA = priKeyCA * curve.g

PUCA = open("PUCA.txt", "w")
# PUCA.write("CA Public key:\nX: " + str(pubKeyCA.x) + "\nY: " + str(pubKeyCA.y))
PUCA.write("CA Private key: " + str(priKeyCA) + "\n")
PUCA.write("CA Public key: " + str(field.displayPoint(pubKeyCA)))

request = open("package1.txt", "r")
package2 = open("package2.txt", "w")

requestRead = request.read()
package2.write(requestRead + "\n")

sign = signature.ECC_sign(requestRead, priKeyCA)

package2.write(str(sign))
package2.close()
