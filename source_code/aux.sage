from sage.all import *
from sqisign_parameters import *

aux_64 = int("ffffffffffffffff",16)
aux_128 = aux_64 << 64
aux_192 = aux_64 << 128
aux_256 = aux_64 << 192
word_size = 16 #word_size in hex digits == 64bits

p_cofactor_for_2f = int("00069c53c50d72bb318674d50cb0e80e86e4a593c926aa29",16)

P_COFACTOR_FOR_2F_BITLENGTH = 179


def print_word(number):
	print(f"{(number&aux_64)}, {(number&aux_128)>>64}, {(number&aux_192)>>128}, {(number&aux_256)>>192}")


def swap_numb(hex,hex_size):
		array = [0 for i in range(hex_size)]
		for j in range(0,hex_size,2):
			array[j] = hex[hex_size-2-j]
			array[j+1] = hex[hex_size-1-j]
			array[hex_size-2-j] = hex[j]
			array[hex_size-1-j] = hex[j+1]
		hex = ''.join(array)
		return hex
