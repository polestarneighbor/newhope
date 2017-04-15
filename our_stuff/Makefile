CC = /usr/bin/gcc
CFLAGS = -Wall -Wextra -O3 -fomit-frame-pointer -msse2avx -march=corei7-avx

HEADERS = $(addprefix $(DIR),  crypto_stream_chacha20.h params.h poly.h randombytes.h ntt.h error_correction.h reduce.h)
CFILES  = $(addprefix $(DIR), crypto_stream_chacha20.c poly.c ntt.c precomp.c randombytes.c error_correction.c newhope.c reduce.c fips202.c)
DIR = ../ref/
all:	nh_computea nh_computesig

nh_computea: $(HEADERS) $(CFILES) nh_computea.c
	$(CC) $(CFLAGS) $(CFILES) nh_computea.c -o $@

nh_computesig: $(HEADERS) $(CFILES) nh_computesig.c
	$(CC) $(CFLAGS) $(CFILES) nh_computesig.c -o $@

.PHONY: clean

clean:
	-rm nh_computea
	-rm nh_computesig
