from base64 import b64decode, encodebytes

import rsa

with open('./utils/RSA/public.pem', 'rb') as p:
    publicKey = rsa.PublicKey.load_pkcs1(p.read())

with open('./utils/RSA/private.pem', 'rb') as p:
    privateKey = rsa.PrivateKey.load_pkcs1(p.read())


def RsaDecrypt(data: str) -> str:
    return rsa.decrypt(b64decode(data.replace(' ', '+')), privateKey).decode('utf-8')


def RsaEncrypt(data: str) -> str:
    return encodebytes(rsa.encrypt(data.encode('utf-8'), publicKey)).decode('utf-8')
