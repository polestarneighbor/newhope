NEWHOPE_SEEDBYTES=32
PARAM_Q=12289
PARAM_N=1024
from polynomial import *
def encode_a(poly, seed):
  s=poly_tobytes(filename,poly)
  return s+seed

def decode_a(senda):
  p,ind =poly_frombytes(senda)
  return p,senda[ind:]

def poly_frombytes(p):
    a=[]
    for l in p:
        a.append(ord(l))
    i=0
    coeffs=[]
    while i<PARAM_N//4:
        coeffs[4*i+0] = a[7*i+0] | ((a[7*i+1]%2**16 & 0x3f) << 8)
        coeffs[4*i+1] = (a[7*i+1] >> 6) | ((a[7*i+2]) << 2) | ((a[7*i+3]%2**16 & 0x0f) << 10)
        coeffs[4*i+2] = (a[7*i+3] >> 4) | ((a[7*i+4]) << 4) | ((a[7*i+5]%2**16 & 0x03) << 12)
        coeffs[4*i+3] = (a[7*i+5] >> 2) | ((a[7*i+6]) << 6)
        i+=1
    return Polynomial(coeffs=coeffs,mod=PARAM_Q,degree=PARAM_N,sizelimit=0)
def poly_tobytes(p):
    s+=''
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

      s+= chr(t0 & 0xff)
      s+= chr((t0 >> 8) | (t1 << 6))
      s+= chr((t1 >> 2))
      s+= chr((t1 >> 10) | (t2 << 4))
      s+= chr((t2 >> 4))
      s+= chr((t2 >> 12) | (t3 << 2))
      s+= chr((t3 >> 6))
    return s


def barrett_reduce(num):
  u = (num * 5) >> 16;
  u *= PARAM_Q
  a -= u
  return a

def poly_frombytes(contents):
  coeffs=[]
  for i in range(0,PARAM_N*2,2):
     coeffs+=chr_to_int(contents[i:i+2])
  return Polynomial(coeffs=coeffs, degree=PARAM_N,mod=PARAM_Q)

import subprocess
from subprocess import PIPE
def get_a():
  signal=subprocess.run(['nh_computea'], stdout=PIPE)
  poly=signal[:PARAM_N*2]
  seed=signal[PARAM_N*2:]
  return poly_frombytes(poly),seed

def get_signal(seed,k):
  coeffs=[0]*(PARAM_N-1)
  coeffs+=[k]
  polyA=poly_tobytes(Polynomial(coeffs=coeffs,mod=PARAM_Q,degree=PARAM_N))
  sendA=polyA+seed
  signal=subprocess.run(['nh_computesig'], stdout=PIPE, stdin=PIPE, input=sendA)
