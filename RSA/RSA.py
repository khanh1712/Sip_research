import binascii, secrets

def inverseMod(d, n):
    t, newt = 0, 1
    r, newr = n, d
    
    while(newr != 0):
        q = r // newr
        r, newr = newr, (r % newr)
        t, newt = newt, (t - q*newt)
    if r > 1:
        print("not in vertible")
    else:
        if (t < 0):
            t += n
        return int(t)

def encrypt_RSA(key, n, msg):
    msg = binascii.hexlify(msg)
    msg = int(msg, 16)
    ciphertext = pow(msg, key, n)
    return ciphertext

def decrypt_RSA(key, n, ciphertext):
    msg = pow(ciphertext, key, n)
    return msg

def createCert(CA_PriKey, n, msg):
    cert = encrypt_RSA(CA_PriKey, n, msg)
    return cert

def decryptCert(CA_PubKey, n, cert):
    msg = decrypt_RSA(CA_PubKey, n, cert)
    return msg


p = 3369993333393829974333376885877453834204643052817571560137951281149
q = 6739986666787659948666753771754907668409286105635143120275902562187

n = p * q
fi = (p-1) * (q-1)
pubKey = secrets.randbelow(fi)
priKey = inverseMod(pubKey, fi)

msg = b"khanh"
hexMsg = binascii.hexlify(msg)
decMsg = int(hexMsg, 16)
print("Msg: ", msg)
print("dec msg: ",decMsg)

encryptedMsg = encrypt_RSA(pubKey, n, msg)
print("Encrypted Msg", encryptedMsg)

decryptedMsg = decrypt_RSA(priKey, n, encryptedMsg)
print("Decrypt Msg", decryptedMsg)


