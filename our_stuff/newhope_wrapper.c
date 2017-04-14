#include "../../avx2/newhope.h"
#include "../../avx2/poly.h"
#include "../../avx2/randombytes.h"
#include "../../avx2/crypto_stream_chacha20.h"
#include "../../avx2/error_correction.h"
#include <math.h>
#include <stdio.h>
#include <string.h>

int main(){
  poly sk_a, pk_a,  pk_adv;
  //pk_adv=convert whatever poly python writes to pipe
  unsigned char python_arg[POLY_BYTES]
  scanf("%s", python_arg);
  poly_frombytes(&pk_adv, python_arg)
  unsigned char key_a[32], key_b[32];
  unsigned char senda[NEWHOPE_SENDABYTES];
  unsigned char sendb[NEWHOPE_SENDBBYTES];
  unsigned char seed[NEWHOPE_SEEDBYTES];
  newhope_keygen(senda, &sk_a);
  decode_a(&pk_a,seed, senda);
  encode_a(senda, &pk_adv, seed);
  //Bob derives a secret key and creates a response
  newhope_sharedb(key_b, sendb, senda);
  poly bp, c;
  printf(sendb);
  // write *bp and *c to a file somehow
  return 0;
}
