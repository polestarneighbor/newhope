NEWHOPE_SEEDBYTES=32
PARAM_Q=12289
PARAM_N=1024
def encode_a(filename, poly, seed):
  poly_tobytes(filename,poly)
  file1=open(filename,'a')
  file1.write(seed)
  file1.close()

def decode_a(filename):
  p=poly_frombytes(filename)
  with open('filename','r') as file1:
    file1.read(PARAM_N*2)
    seed=file1.read()
  return p,seed

def barrett_reduce(num):
  u = int(num) * 5) >> 16;
  u *= PARAM_Q
  a -= u
  return a

def poly_tobytes(filename,poly):
  i=0
  file1=open(filename,'w')
  while i<poly.degree:
    file1.write(int_to_chr(poly.coeffs[i]))
    i+=1
  file1.close()

def int_to_chr(num1):
  num1=num//256
  num2=num%256
  return chr(num1)+chr(num2)
def chr_to_int(chrs):
  num1=ord(chrs[0])
  num2=ord(chrs[1])
  return num1*256+num2
def poly_frombytes(filename):
  file1=open(filename,'r')
  coeffs=[]
  contents=filename.read(PARAM_N*2)
  for i in range(0,PARAM_N*2,2):
     coeffs+=chr_to_int(contents[i:i+2])
  return Polynomial(coeffs=coeffs, degree=PARAM_N,mod=PARAM_Q)
