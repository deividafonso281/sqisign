from sqisign_parameters import prime
from sage.all import *

p = prime()

Fp2.<im_unity> = FiniteField(p**_sage_const_2 ,'im_unity',modulus=var('x')**2  + 1 )

print(Fp2)
