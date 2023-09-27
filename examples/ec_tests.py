import x25519
import ed25519
import time 
import random

# this function allows the test to work on CPython or micropython
try:
    ticks_us = time.ticks_us
except:
    # cpython case
    def ticks_us():
        return time.time()*1000000
    
try:
    from gc import collect as _collect
    from gc import mem_alloc

    def collect():
        before = mem_alloc()
        _collect()
        after = mem_alloc()
        print(f"collect : {before} -> {after}")
except:
    def collect():
        pass

def timeit(name, func, *args):
    t1 = ticks_us()
    output = func(*args)
    t2 = ticks_us()
    delta = t2-t1
    unit = "us"
    if delta > 1000:
        delta = delta/1000
        unit = "ms"
    if delta > 1000:
        delta = delta/1000
        unit = "s"
    print(f"{name} ({func}) : {delta} {unit}")
    return output

def token_bytes(length:int)->bytes:
    output = []
    for i in range(length):
        output.append(random.randint(0,255))

    return bytes(output)

# Ed22519

def test_ed25519():
    print("start of test_ed25519")
    collect()
    secret_key = token_bytes(32)
    print("stating Public key generation")
    print(f"Private key : {secret_key}")
    pk = timeit("ed25519:create public key", ed25519.publickey_unsafe, secret_key)
    print(f"Public key : {pk}")

    message=b"hello"
    sign = timeit("ed25519:sign", ed25519.signature_unsafe, message, secret_key, pk)
    print(f"signature : {sign}")

    timeit("ed25519:check signature", ed25519.checkvalid, sign, message, pk)
    print("end of test_ed25519")

test_ed25519()

def test_x25519():
    print("start of test_x25519")
    collect()
    secret_key = token_bytes(32)
    secret_key2 = token_bytes(32)

    sk = timeit("x25519:private key from bytes", x25519.X25519PrivateKey.from_private_bytes, secret_key)
    pk = timeit("x25519:public key from private one", sk.public_key)

    sk2 = x25519.X25519PrivateKey.from_private_bytes(secret_key2)
    pk2 = sk2.public_key()

    ss = timeit("x25519:exchange", sk.exchange, pk2)

    ss2 = sk2.exchange(pk)
    print(f"{ss} ==? {ss2}")
    print("end of test_x25519")

test_x25519()

