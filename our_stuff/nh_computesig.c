#include "../../avx2/newhope.h"
#include "../../avx2/poly.h"
#include "../../avx2/randombytes.h"
#include "../../avx2/crypto_stream_chacha20.h"
#include "../../avx2/error_correction.h"
#include <math.h>
#include <stdio.h>
#include <string.h>

#include <fcntl.h>
#include <stdio.h>
#include <sys/stat.h>
#include <unistd.h>

#define MAX_BUF 1024

  int main(){
    poly sk_a, pk_a,  pk_adv;
    unsigned char key_a[32], key_b[32];
    unsigned char senda[NEWHOPE_SENDABYTES];
    unsigned char sendb[NEWHOPE_SENDBBYTES];
    unsigned char seed[NEWHOPE_SEEDBYTES];

    // read senda from pipe
    int pipe_a;
    char * senda_pipe = "/tmp/senda";
    char buf[MAX_BUF];

    // open and read from the pipe
    pipe = open(senda_pipe, O_RDONLY);
    read(pipe, buf, MAX_BUF);
    close(pipe);
    scanf("%s",senda);

    newhope_sharedb(key_b,sendb,senda)

    // write sendb to pipe
    int pipe_b;
    char * sendb_pipe = "/tmp/sendb";

    // create the pipe
    mkfifo(sendb_pipe, 0666);

    // write sendb to the FIFO
    printf(sendb);
    pipe_b = open(sendb_pipe, O_WRONLY);
    write(pipe_b, sendb, sizeof(sendb));
    close(pipe_b);

    // remove the pipe
    unlink(sendb_pipe);

    return 0;
  }
