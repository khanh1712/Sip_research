import field
from tinyec import registry
import signature

samplecurve = registry.get_curve("brainpoolP256r1")
p = samplecurve.field.p
a = samplecurve.a
b = samplecurve.b
x_g = samplecurve.g.x
y_g = samplecurve.g.y
n = samplecurve.field.n
curve = field.Curve(a, b, p, n, x_g, y_g)

file = open("Server.txt", "r")
fileRead = file.readlines()
x = field.Point(curve, field.getPoint(fileRead[2])[0], field.getPoint(fileRead[2])[1])
print(field.displayPoint(x))

