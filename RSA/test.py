import binascii, secrets
from functions import inverseMod
import RSA

p = 3369993333393829974333376885877453834204643052817571560137951281149  
q = 6739986666787659948666753771754907668409286105635143120275902562187   

n = p * q
fi = (p-1) * (q-1)
pubKey = secrets.randbelow(fi)
priKey = int(inverseMod(pubKey, fi))

msg = b"khanh"
hexMsg = binascii.hexlify(msg)
decMsg = int(hexMsg, 16)
print("Msg: ", msg)
print("dec msg: ",decMsg)

encryptedMsg = RSA.encrypt_RSA(pubKey, n, msg)
print("Encrypted Msg", encryptedMsg)

decryptedMsg = RSA.decrypt_RSA(priKey, n, encryptedMsg)
print("Decrypt Msg", decryptedMsg)
