from sage.all import *

aux_64 = int("ffffffffffffffff",16)
aux_128 = aux_64 << 64
aux_192 = aux_64 << 128
aux_256 = aux_64 << 192

def print_word(number):
	print(f"{(number&aux_64)}, {(number&aux_128)>>64}, {(number&aux_192)>>128}, {(number&aux_256)>>192}")
