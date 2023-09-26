# https://ed25519.cr.yp.to/python/ed25519.py
# code published on 2017
# I need to rework 
# * integer division (//)
# * supported hash
# * use bytes instead of str

import hashlib

b = 256
q = 2**255 - 19
l = 2**252 + 27742317777372353535851937790883648493

def H(m):
  # Use this trick to support sha256 instead of sha512
  # (sha512 is not available on micropython)
  h1 = hashlib.sha256(m).digest()
  h2 = hashlib.sha256(h1).digest()
  return h1+h2

def expmod(b,e,m):
  if e == 0: return 1
  t = expmod(b,e//2,m)**2 % m
  if e & 1: t = (t*b) % m
  return t

def inv(x):
  return expmod(x,q-2,q)

# originally, the I value is calculated on module loading but is required heavy recursion, not supported by micropython
#I = expmod(2,(q-1)//4,q)
# d = -121665 * inv(121666)
d = -4513249062541557337682894930092624173785641285191125241628941591882900924598840740
I = 19681161376707505956807079304988542015446066515923890162744021073123829784752

def xrecover(y):
  xx = (y*y-1) * inv(d*y*y+1)
  x = expmod(xx,(q+3)//8,q)
  if (x*x - xx) % q != 0: x = (x*I) % q
  if x % 2 != 0: x = q-x
  return x

# By = 4 * inv(5)
# Bx = xrecover(By)
By = 46316835694926478169428394003475163141307993866256225615783033603165251855960
Bx = 15112221349535400772501151409588531511454012693041857206046113283949847762202
B = [Bx % q,By % q]

def edwards(P,Q):
  x1 = P[0]
  y1 = P[1]
  x2 = Q[0]
  y2 = Q[1]
  x3 = (x1*y2+x2*y1) * inv(1+d*x1*x2*y1*y2)
  y3 = (y1*y2+x1*x2) * inv(1-d*x1*x2*y1*y2)
  return [x3 % q,y3 % q]

def scalarmult(P,e):
  if e == 0: return [0,1]
  Q = scalarmult(P,e//2)
  Q = edwards(Q,Q)
  if e & 1: Q = edwards(Q,P)
  return Q

def encodeint(y):
  bits = [(y >> i) & 1 for i in range(b)]
  return bytes([sum([bits[i * 8 + j] << j for j in range(8)]) for i in range(b//8)])

def encodepoint(P):
  x = P[0]
  y = P[1]
  bits = [(y >> i) & 1 for i in range(b - 1)] + [x & 1]
  return bytes([sum([bits[i * 8 + j] << j for j in range(8)]) for i in range(b//8)])

def bit(h,i):
  return (h[i//8] >> (i%8)) & 1

def publickey(sk):
  h = H(sk)
  a = 2**(b-2) + sum(2**i * bit(h,i) for i in range(3,b-2))
  A = scalarmult(B,a)
  return encodepoint(A)

def Hint(m):
  h = H(m)
  return sum(2**i * bit(h,i) for i in range(2*b))

def signature(m,sk,pk):
  h = H(sk)
  a = 2**(b-2) + sum(2**i * bit(h,i) for i in range(3,b-2))
  r = Hint(bytes([h[i] for i in range(b//8,b//4)]) + m)
  R = scalarmult(B,r)
  S = (r + Hint(encodepoint(R) + pk + m) * a) % l
  return encodepoint(R) + encodeint(S)

def isoncurve(P):
  x = P[0]
  y = P[1]
  return (-x*x + y*y - 1 - d*x*x*y*y) % q == 0

def decodeint(s):
  return sum(2**i * bit(s,i) for i in range(0,b))

def decodepoint(s):
  y = sum(2**i * bit(s,i) for i in range(0,b-1))
  x = xrecover(y)
  if x & 1 != bit(s,b-1): x = q-x
  P = [x,y]
  if not isoncurve(P): raise Exception("decoding point that is not on curve")
  return P

def checkvalid(s,m,pk):
  if len(s) != b//4: raise Exception("signature length is wrong")
  if len(pk) != b//8: raise Exception("public-key length is wrong")
  R = decodepoint(s[0:b//8])
  A = decodepoint(pk)
  S = decodeint(s[b//8:b//4])
  h = Hint(encodepoint(R) + pk + m)
  if scalarmult(B,S) != edwards(R,scalarmult(A,h)):
    raise Exception("signature does not pass verification")