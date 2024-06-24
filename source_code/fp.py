from sqisign_parameters import *
from aux import *


def fp_add(numb1,numb2):
        return (numb1+numb2) % prime()


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


def fp_inv(numb):
    exponent = prime - 2
    exponent = bin(exponent)
    acc = numb
    out = fiat_p1913_to_montgomery(1)
    for i in range(len(exponent)-1,1,-1):
        if (int(exponent[i])) == 1:
            out = fiat_p1913_mul(acc,out)
        acc = fp_square(acc)
    
    return out


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


def fp_square(numb):
    return fiat_p1913_mul(numb,numb)


def fp_sub(numb1,numb2):
    if numb1 < numb2:
        return (prime() + numb1 - numb2) % prime()
    return (numb1 - numb2) % prime()


def fiat_p1913_set_one():

	return int("2c75875e51a899cf31655e69e2fe2f236b4d86db2abae0000000000000000004",16)
