import random
import x25519

def token_bytes(length:int)->bytes:
    output = []
    for i in range(length):
        output.append(random.randint(0,255))

    return bytes(output)

print("start")
secret_key = token_bytes(32)
print("secret 1")
secret_key2 = token_bytes(32)
print("secret 1")

sk = x25519.X25519PrivateKey.from_private_bytes(secret_key)
print("sk 1")
pk = sk.public_key()
print("pk 1")


sk2 = x25519.X25519PrivateKey.from_private_bytes(secret_key2)
print("sk 2")
pk2 = sk2.public_key()
print("pk 2")

ss = sk.exchange(pk2)
print("ss")
ss2 = sk2.exchange(pk)
print("ss2")

print(ss)
print(ss2)