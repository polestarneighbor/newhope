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
  //pk_adv=convert whatever poly python sends as arg
  unsigned char key_a[32], key_b[32];
  unsigned char senda[NEWHOPE_SENDABYTES];
  unsigned char seed[NEWHOPE_SEEDBYTES];
  newhope_keygen(senda, &sk_a);
  //write senda to pipe
  return 0;
}
