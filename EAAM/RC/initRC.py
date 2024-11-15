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

priKey = randint(pow(2,255), pow(2,256))
pubKey = priKey*curve.g
id = 678910

groupKey = randint(pow(2,255), pow(2,256))

RC = open("RC.txt", "w")
server = open("Server.txt", "a")

# RC.write("ID: "+str(id)+"\nPrivate key: "+str(priKey)+"\nPublic key: \nX: "+str(pubKey.x)+"\nY: "+str(pubKey.y))
RC.write("ID: "+str(id)+"\nPrivate key: "+str(priKey)+"\nPublic key: "+str(field.displayPoint(pubKey)))
RC.write("\nGroup key: " + str(groupKey))
server.write("\nGroup key: " + str(groupKey))

RC.close()
server.close()
