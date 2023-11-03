import json
import os
import base64
import pyDes

work_dir = os.getcwd()
# 加载密钥信息
crypto_file = os.path.join(work_dir, 'crypto.json')

if os.path.exists(crypto_file):
    with open(crypto_file, "r+") as fn:
        cryptoParams = json.load(fn)

if not os.path.exists(crypto_file):
    def normalize_value(input: str):
        if input.startswith(CryptoObject.CRYPTO_CONST):
            raise RuntimeError('未找到配置文件解密密钥')
        return input
else:
    def normalize_value(input: str):
        if not input.startswith(CryptoObject.CRYPTO_CONST):
            return input
        return CryptoObject(input, lambda x: cryptoParams)

CRYPTO_CONST = '{crypto}'


def as_password_value(input: str):
    return PasswordObject(input)


def as_crypto_value(input: str):
    if cryptoParams is None:
        raise RuntimeError('未找到配置文件解密密钥')
    return CryptoObject(input, lambda x: cryptoParams)


class SecurityObject(object):
    def __init__(self, data: str):
        super().__init__()
        self._data = data

    def toString(self):
        raise RuntimeError('not implemented')

    def toJSON(self):
        return '***************'


class CryptoObject (SecurityObject):
    def __init__(self, data: str, cb):
        super().__init__(data)
        self._cb = cb

    def __str__(self):
        o = self._cb()
        hexKey = base64.decodestring(o['key'])
        hexIV = base64.decodestring(o['iv'])
        cipher_data = base64.decodestring(self._data)
        algo = pyDes.triple_des(
            hexKey, pyDes.CBC, IV=hexIV, pad=None, padmode=pyDes.PAD_PKCS5)
        plain_text = str(algo.decrypt(cipher_data), 'utf-8')
        return plain_text

    # __repr__ = __str__


class PasswordObject(SecurityObject):
    def __init__(self, data: str):
        super().__init__(data)

    def __str__(self):
        return str(self._data)

    # __repr__ = __str__
