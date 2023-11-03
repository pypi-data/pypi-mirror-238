import base64
import pyDes

key = '0em6gPy28I3PKThIcjn1cMITCOnKGjjl'
iv = 'lJ7nEAhiSBk='

hexKey = base64.standard_b64decode(key)
hexIV = base64.standard_b64decode(iv)


cipher_text = '+gCbLGcOx9dPerONJqwzpkVy6+9DN4lukPOV4Dc6kmk='

algo = pyDes.triple_des(hexKey, pyDes.CBC, IV=hexIV)

cipher_data = base64.standard_b64decode(cipher_text)
plain_data = algo.decrypt(cipher_data, pad=None, padmode=pyDes.PAD_PKCS5)
# print(plain_data)
plain_text = plain_data.decode("utf-8")
print(plain_text)
