CC = /usr/bin/gcc
CFLAGS = -Wall -Wextra -O3 -fomit-frame-pointer -msse2avx -march=corei7-avx

HEADERS = crypto_stream_chacha20.h params.h poly.h randombytes.h ntt.h error_correction.h reduce.h
CFILES  = ../ref/crypto_stream_chacha20.c poly.c ntt.c precomp.c error_correction.c newhope.c reduce.c fips202.c
DIR = ../ref
CFILES = $(addprefix $(DIR) $(CFILES))
HEADERS = $(addprefix $(DIR) $(HEADERS))
all:	nh_computea
			nh_computesig

nh_computea: $(HEADERS) $(CFILES) nh_computea.c
	$(CC) $(CFLAGS) $(CFILES) nh_computea.c -o $@

nh_computesig: $(HEADERS) $(CFILES) nh_computesig
	$(CC) $(CFLAGS) $(CFILES) nh_computesig -o $@

.PHONY: clean

clean:
	-rm nh_computea
	-rm nh_computesig
