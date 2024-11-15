import Hash
import field
import signature
from tinyec import registry

samplecurve = registry.get_curve("brainpoolP256r1")
p = samplecurve.field.p
a = samplecurve.a
b = samplecurve.b
x_g = samplecurve.g.x
y_g = samplecurve.g.y
n = samplecurve.field.n
curve = field.Curve(a, b, p, n, x_g, y_g)

# Open package 3
package3 = open("package3.txt", "r")
RC = open("RC.txt", "r")
package4 = open("package4.txt", "w")
PUCA = open("PUCA.txt", "r")

package3Read = package3.readlines()
RCRead = RC.readlines()
PUCARead = PUCA.readlines()

r = int(RCRead[1][13:])
Tl = field.Point(curve, field.getPoint(package3Read[8])[0], field.getPoint(package3Read[8])[1])
Trl = r * Tl
TrlKey = Hash.bytes_to_long(Hash.hash_function(str(Trl.x)))
TlrKey = int(package3Read[0][9:])


# Check if Trl == Tlr (chua co ham ma doi xung). If valid, extract info and operate
if TrlKey == TlrKey:
    k1 = int(package3Read[1][5:])
    Fi = int(package3Read[2][5:])
    Ti = field.Point(curve, field.getPoint(package3Read[3])[0], field.getPoint(package3Read[3])[1])
    IDi = int(package3Read[4][6:])

    message = package3Read[5] + package3Read[6][0: -1]   
    signCA = (field.getPoint(package3Read[7])[0], field.getPoint(package3Read[7])[1])
    pubKeyCA = field.Point(curve, field.getPoint(PUCARead[1])[0], field.getPoint(PUCARead[1])[1])
        
    # calculate Tir = Tri to check k1
    Tri = r * Ti
    k1Key = Hash.bytes_to_long(Hash.hash_function(str(Tri.x) + str(IDi)))

    # check validity of k1 and cert then create materials
    if (k1 == k1Key and signature.ECC_verify_sign(message, signCA, pubKeyCA) == True):
        groupKey = int(RCRead[3][11:])
        priKeyRC = int(RCRead[1][13:])
        Ai = Hash.hash_function(str(IDi) + str(groupKey))
        Bi = Hash.bytes_to_long(Ai) ^ groupKey
        Ci = Hash.bytes_to_long(Hash.hash_function(Ai))
        k2 = Hash.bytes_to_long(Hash.hash_function(str(Trl.x) + str(IDi)))
        sig = Hash.hash_function(str(groupKey) + str(Bi) + str(Ti.x))
        sigRC = signature.ECC_sign(sig, priKeyRC)

        package4.write("k2 = " + str(k2))
        package4.write("\nBi = " + str(Bi))
        package4.write("\nCi = " + str(Ci))
        package4.write("\nRC signature: " + str(sigRC))

    else:
        print("Invalid user")
else:
    print("Invalid package")

# close files
package3.close()
package4.close()
RC.close()
PUCA.close()