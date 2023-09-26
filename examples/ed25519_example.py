import ed25519
import secrets


secret_key = secrets.token_bytes(32)

pk = ed25519.publickey(secret_key)
print(pk)
message=b"hello"
sign = ed25519.signature(message, secret_key, pk)
print(sign)

ed25519.checkvalid(sign, message, pk)
