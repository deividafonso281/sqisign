from sage.all import *
from sqisign_parameters import *
from finite_field import *

aux_64 = int("ffffffffffffffff",16)
aux_128 = aux_64 << 64
aux_192 = aux_64 << 128
aux_256 = aux_64 << 192
word_size = 16 #word_size in hex digits == 64bits

p_cofactor_for_2f = int("00069c53c50d72bb318674d50cb0e80e86e4a593c926aa29",16)

P_COFACTOR_FOR_2F_BITLENGTH = 179

def re(numb):
	if len(numb.polynomial().coefficients()) == 0:
		return 0
	else:
		return int(numb.polynomial().coefficients()[0])


def im(numb):
	if len(numb.polynomial().coefficients()) <= 1:
		return 0
	else:
		return int(numb.polynomial().coefficients()[1])


def add_point(p1,p2,p1_p2):
	v1 = fp2_mul((p1[0]+p1[1]),(p2[0]-p2[1]))
	v2 = fp2_mul((p1[0]-p1[1]),(p2[0]+p2[1]))
	v3 = (v1 + v2)
	v3 = fp2_sqr(v3)
	v4 = (v1 - v2)
	v4 = fp2_sqr(v4)
	xplus = fp2_mul(p1_p2[1],v3)
	zplus = fp2_mul(p1_p2[0],v4)
	
	return (xplus,zplus) 


def double_point(point, A24):
	q = [0,0]
	t0 = (point[0] + point[1])
	t0 = fp2_sqr(t0)
	t1 = (point[0] - point[1])
	t1 = fp2_sqr(t1)
	t2 = (t0 - t1)
	t1 = fp2_mul(t1,A24[1])
	q[0] = fp2_mul(t0,t1)
	t0 = fp2_mul(t2,A24[0])
	t0 = (t0+t1)
	q[1] = fp2_mul(t0,t2)
	
	return (q[0],q[1])


def mult_scalar_point(point, scalar,A24):
	x0 = point
	x1 = double_point(x1,A24)
	for i in range(178,-1,-1):
		k = (scalar >> i) & 1
		print(f"k: {k}") 
		#k = int(scalar_binary[i])
		if k == 0:
			x0_new = double_point(x0,A24)
			x1_new = add_point(x0,x1,point)
		else:
			x0_new = add_point(x0,x1,point)
			x1_new = double_point(x1,A24)
		x0 = x0_new
		x1 = x1_new
		print_word(re(x1[0]))
		print_word(im(x1[0]))
		print_word(re(x1[1]))
		print_word(im(x1[1]))
	
	return x0


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


def fiat_p1913_to_montgomery(numb):
	x3 = (numb & aux_256) >> 192
	x2 = (numb & aux_192) >> 128
	x1 = (numb & aux_128) >> 64
	x4 = (numb & aux_64)
	r1 = x4*montgomery()
	r2 = (r1 & aux_64) * prime()
	r3 = x1 * montgomery()
	r4 = ((r1+r2)>>64) + r3
	r5 = (((r4 & aux_64) * prime() + r4) >> 64) + x2 * montgomery()
	r6 = (r5 & aux_64) * prime() + r5
	r7 = x3 * montgomery()
	r8 = (r6 >> 64) + r7
	r9 = (r8 & aux_64) * prime() + r8
		
	return (r9 >> 64)% prime()	

def fiat_p1913_from_montgomery(numb):
	x0 = numb & aux_64
	x1 = (numb & aux_128) >> 64
	x2 = (numb & aux_192) >> 128
	x3 = (numb & aux_256) >> 192
	r0 = ((x0 * prime() + x0) >> 64) + x1
	r1 = (((r0 & aux_64) * prime() + r0) >> 64) + x2
	r2 = (((r1 & aux_64) * prime() +r1) >> 64) + x3
	r3 = ((r2 & aux_64) * prime() + r2) >> 64
		
	return r3 % prime()


def fiat_p1913_mul(numb1, numb2):
	x0 = numb1 & aux_64
	x1 = (numb1>>64) & aux_64
	x2 = (numb1>>128) & aux_64
	x3 = (numb1>>192) & aux_64
	r1 = x0*numb2
	r2 = (r1 & aux_64) * prime()
	r3 = r1 + r2
	r4 = x1 * numb2
	r5 = (r3 >> 64) + r4
	r6 = (r5 & aux_64) * prime()
	r7 = r6 + r5
	r8 = x2 * numb2
	r9 = r8 + (r7>>64)
	r10 = (r9 & aux_64)* prime()
	r11 = r10 + r9
	r12 = x3 * numb2
	r13 = (r11 >> 64) + r12
	r14 = (r13 & aux_64) * prime()
	return ((r13+r14)>>64)% prime()


def fp_square(numb):
	return fiat_p1913_mul(numb,numb)


def fiat_p1913_set_one():
		
	return int("2c75875e51a899cf31655e69e2fe2f236b4d86db2abae0000000000000000004",16)


def fp2_is_square(numb):
	r1 = fp_square(re(numb))
	r2 = fp_square(im(numb))
	r1 = (r1 + r2) % prime()
	return fp_is_square(r1)


def fp2_mul(numb1,numb2):
	
	r1 = (re(numb1)+im(numb1))%prime()
	r2 = (re(numb2)+im(numb2))%prime()
	r1 = fiat_p1913_mul(r1, r2)
	r2 = fiat_p1913_mul(im(numb1), im(numb2))
	r3 = fiat_p1913_mul(re(numb1), re(numb2))
	r4 = r1 - r2 - r3
	r5 = r3 - r2
	return r5 + r4*im_unity


def fp2_sqr(numb):
	return fp2_mul(numb,numb)


def fp_is_square(numb):
	exponent = prime() >> 1
	exponent = bin(exponent)
	acc = numb
	out = fiat_p1913_to_montgomery(1)
	for i in range(len(exponent)-1,1,-1):
		if int(exponent[i]) == 1:
			out = fiat_p1913_mul(acc, out)
		acc = fp_square(acc)
	
	return fiat_p1913_from_montgomery(out) == 1
