from Crypto.Cipher import AES
import base64
from hashlib import md5

BLOCK_SIZE = 16

def unpad(data):
    return data[:-(data[-1] if type(data[-1]) == int else ord(data[-1]))]

def bytes_to_key(data, salt, output=48):
    assert len(salt) == 8, len(salt)
    data += salt
    key = md5(data).digest()
    final_key = key
    while len(final_key) < output:
        key = md5(key + data).digest()
        final_key += key
    return final_key[:output]

def decrypt(encrypted):
    encrypted = base64.b64decode(encrypted)
    assert encrypted[0:8] == b"Salted__"
    salt = encrypted[8:16]
    key_iv = bytes_to_key("ApiKeySecret".encode(), salt, 32+16)
    key = key_iv[:32]
    iv = key_iv[32:]
    aes = AES.new(key, AES.MODE_CBC, iv)
    decrypted_thing = (unpad(aes.decrypt(encrypted[16:]))).decode('utf-8')
    return decrypted_thing

encrypted_thing = "U2FsdGVkX1+8IwMz9h+CMUcyJt5zwIzatNzLijkOa7ztUZFn0/ESXyYhx8GYap+6dB+MhsslivCuUuPmK19Z9+l7shKGuWFQ9Rkts48BFYhqxzZg0KDHbZNPkKW4q55j"

print(decrypt(encrypted_thing))
