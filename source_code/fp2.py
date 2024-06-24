from sqisign_parameters import *
from aux import *
from fp import *


class fp2_t:
    def __init__(self,re,im):
        self.re = re
        self.im = im

    def print_fp2(self):
        print(f"re = ",end="")
        print_word(self.re)
        print(f"im = ",end="")
        print_word(self.im)


def fp2_add(numb1,numb2):
    re = fp_add(numb1.re,numb2.re)
    im = fp_add(numb1.im,numb2.im)
    return fp2_t(re,im)


def fp2_sub(numb1,numb2):
    re = fp_sub(numb1.re,numb2.re)
    im = fp_sub(numb1.im,numb2.im)
    return fp2_t(re,im)


def fp2_is_square(numb):
	r1 = fp_square(numb.re)
	r2 = fp_square(numb.im)
	r1 = fp_add(r1,r2)
	return fp_is_square(r1)


def fp2_mul(numb1,numb2):
    r1 = fp_add(numb1.re,numb1.im)
    r2 = fp_add(numb2.re,numb2.im)
    r1 = fiat_p1913_mul(r1, r2)
    r2 = fiat_p1913_mul(numb1.im, numb2.im)
    r3 = fiat_p1913_mul(numb1.re, numb2.re)
    r4 = fp_sub(r1, r2)
    r5 = fp_sub(r4, r3)
    r6 = fp_sub(r3, r2)
    return fp2_t(r6,r5)


def fp2_sqr(numb):
    return fp2_mul(numb,numb)


def fp2_sub(numb1,numb2):
    re = fp_sub(numb1.re,numb2.re)
    im = fp_sub(numb1.im,numb2.im)
    return fp2_t(re,im)


def fp2_add(numb1,numb2):
    re = fp_add(numb1.re,numb2.re)
    im = fp_add(numb1.im,numb2.im)
    return fp2_t(re,im)


def fp2_is_zero(numb):
    if numb.re == 0 and numb.im == 0:
        return True
    return False
