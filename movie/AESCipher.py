#!/usr/bin/env python

from Crypto.Cipher import AES
import hashlib
import base64
from Crypto.Util import Padding

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s: s[0:-ord(s[-1])]


class AESCipher:
    def __init__(self, password):
        self.bs = 16
        self.key = self.hash(password)
        self.cipher = AES.new(self.key, AES.MODE_ECB)
        # self.key = self.hash(password)

    def encrypt(self, raw):
        pad_raw = Padding.pad(raw.encode(), self.bs)
        encrypted = self.cipher.encrypt(pad_raw)
        # ciphertext, tag = self.cipher.encrypt(raw.encode())
        encoded = base64.b64encode(encrypted)
        return str(encoded, 'utf-8')

    def decrypt(self, raw):
        decoded = base64.b64decode(raw)
        decrypted = self.cipher.decrypt(decoded)
        return str(Padding.unpad(decrypted, self.bs), 'utf-8')

    def hash(self, password):
        return hashlib.md5(password.encode('utf-8')).hexdigest().encode()
