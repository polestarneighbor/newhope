NEWHOPE_SEEDBYTES=32
POLY_BYTES=1792
NEWHOPE_SENDABYTES=NEWHOPE_SEEDBYTES+POLY_BYTES
REC_BYTES=256
PARAM_Q=12289
PARAM_N=1024
from polynomial import *
def encode_a(poly, seed):
  s=poly_tobytes(poly)
  return s+seed

def decode_a(senda):
  p=poly_frombytes(senda)
  return p,senda[POLY_BYTES:]
def decode_b(sendb):
  coeffs=[0]*REC_BYTES*4
  for i in range(0,REC_BYTES):
    coeffs[4*i+0] =  (sendb[POLY_BYTES+i])& 0x03
    coeffs[4*i+1] = ((sendb[POLY_BYTES+i]) >> 2) & 0x03
    coeffs[4*i+2] = ((sendb[POLY_BYTES+i]) >> 4) & 0x03
    coeffs[4*i+3] = ((sendb[POLY_BYTES+i]) >> 6)
  return Polynomial(coeffs=coeffs,mod=PARAM_Q, degree=PARAM_N)
def poly_frombytes(a):
    i=0
    coeffs=[0]*PARAM_N
    while i<PARAM_N//4:
        coeffs[4*i+0] = a[7*i+0] | ((a[7*i+1]%2**16 & 0x3f) << 8)
        coeffs[4*i+1] = (a[7*i+1] >> 6) | ((a[7*i+2]) << 2) | ((a[7*i+3]%2**16 & 0x0f) << 10)
        coeffs[4*i+2] = (a[7*i+3] >> 4) | ((a[7*i+4]) << 4) | ((a[7*i+5]%2**16 & 0x03) << 12)
        coeffs[4*i+3] = (a[7*i+5] >> 2) | ((a[7*i+6]) << 6)
        i+=1
    return Polynomial(coeffs=coeffs,mod=PARAM_Q,degree=PARAM_N,sizelimit=0)
def poly_tobytes(p):
    s=b''
    for i in range(PARAM_N//4):
      t0 = barrett_reduce(p.coeffs[4*i+0]) #Make sure that coefficients have only 14 bits
      t1 = barrett_reduce(p.coeffs[4*i+1])
      t2 = barrett_reduce(p.coeffs[4*i+2])
      t3 = barrett_reduce(p.coeffs[4*i+3])

      m = t0 - PARAM_Q
      c = m
      c >>= 15
      t0 = m ^ ((t0^m)&c) # <Make sure that coefficients are in [0,q]

      m = t1 - PARAM_Q
      c = m
      c >>= 15
      t1 = m ^ ((t1^m)&c) # <Make sure that coefficients are in [0,q]

      m = t2 - PARAM_Q
      c = m
      c >>= 15
      t2 = m ^ ((t2^m)&c) # <Make sure that coefficients are in [0,q]

      m = t3 - PARAM_Q
      c = m
      c >>= 15
      t3 = m ^ ((t3^m)&c) # <Make sure that coefficients are in [0,q]

      s+= bytes((t0 & 0xff))
      s+= bytes((t0 >> 8) | (t1 << 6))
      s+= bytes((t1 >> 2))
      s+= bytes((t1 >> 10) | (t2 << 4))
      s+= bytes((t2 >> 4))
      s+= bytes((t2 >> 12) | (t3 << 2))
      s+= bytes((t3 >> 6))
    return s


def barrett_reduce(num):
  u = (num * 5) >> 16;
  u *= PARAM_Q
  num -= u
  return num


import subprocess
from subprocess import PIPE
def get_a():
  signal=subprocess.run(['./nh_computea'], stdout=PIPE)
  out=signal.stdout
  err=signal.stderr
  if err!=None:
    print('Fail:',err)
    return
  return decode_a(out[:NEWHOPE_SENDABYTES]),poly_frombytes(out[NEWHOPE_SENDABYTES:])

def get_signal(seed,k):
  coeffs=[k if i == 0 else 0 for i in range(PARAM_N)]
  polyA=Polynomial(coeffs=coeffs,mod=PARAM_Q,degree=PARAM_N)
  sendA=encode_a(polyA,seed)
  signal=subprocess.run(['./nh_computesig'], stdout=PIPE, input=sendA)
  out=signal.stdout
  err=signal.stderr
  if err!=None:
    print('Fail:',err)
    return
  return decode_b(out) 
def main():
  polyseed,a=get_a()
  poly,seed=polyseed
  sig=get_signal(seed,1)
  return sig
main()
