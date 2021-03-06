#include "../ref/newhope.h"
#include "../ref/poly.h"
#include "../ref/randombytes.h"
#include "../ref/crypto_stream_chacha20.h"
#include "../ref/error_correction.h"
#include <math.h>
#include <stdio.h>
#include <string.h>

#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>
#define PARAM_N 1024

int main(){
  poly a, pk_a,sk_a;
  unsigned char senda[NEWHOPE_SENDABYTES];
  unsigned char seed[NEWHOPE_SEEDBYTES];
  unsigned char polya[POLY_BYTES];

  newhope_keygen(senda, &sk_a);
  decode_a(&pk_a, seed, senda);
  gen_a(&a, seed);
  poly_tobytes(polya, &a);

  // write senda and polya to pipe
  //int pipe_a;
  //char * senda_polya_pipe = "/tmp/senda_polya";

  // create the pipe
  //mkfifo(senda_polya_pipe, 0666);

  // write senda to the FIFO
  //pipe_a = open(senda_polya_pipe, O_WRONLY);
  //write(pipe_a, senda, sizeof(senda));
  //write(pipe_a, polya, sizeof(polya));
  if (write(STDOUT_FILENO, senda,sizeof(senda))!=sizeof(senda))
    {
    printf("senda not written");    
    }
  if (write(STDOUT_FILENO, polya, sizeof(polya))!=sizeof(polya))
    {
    printf("senda not written");    
    }
  //close(pipe_a);

  // remove the pipe
 // unlink(senda_pipe);

  return 0;
}
