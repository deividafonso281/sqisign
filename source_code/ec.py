from sqisign_parameters import *
from fp import *
from fp2 import *
from aux import *


def is_point_equal(P,Q):
    if (fp2_is_zero(P[0]) and fp2_is_zero(P[1])) or (fp2_is_zero(Q[0]) and fp2_is_zero(Q[1])):
        return fp2_is_zero(P[0]) and fp2_is_zero(P[1]) and fp2_is_zero(Q[0]) and fp2_is_zero(Q[1])

    t0 = fp2_mul(P[0],Q[1])
    t1 = fp2_mul(P[1],Q[0])
    t0 = fp2_sub(t0,t1)

    return fp2_is_zero(t0)


def add_point(p1,p2,p1_p2):
    v1 = fp2_mul(fp2_add(p1[0],p1[1]),fp2_sub(p2[0],p2[1]))
    v2 = fp2_mul(fp2_sub(p1[0],p1[1]),fp2_add(p2[0],p2[1]))
    v3 = fp2_add(v1,v2)
    v3 = fp2_sqr(v3)
    v4 = fp2_sub(v1,v2)
    v4 = fp2_sqr(v4)
    xplus = fp2_mul(p1_p2[1],v3)
    zplus = fp2_mul(p1_p2[0],v4)
    
    return (xplus,zplus)


def double_point(point, A24):
    q = [0,0]
    t0 = fp2_add(point[0],point[1])
    t0 = fp2_sqr(t0)
    t1 = fp2_sub(point[0],point[1])
    t1 = fp2_sqr(t1)
    t2 = fp2_sub(t0,t1)
    t1 = fp2_mul(t1,A24[1])
    q[0] = fp2_mul(t0,t1)
    t0 = fp2_mul(t2,A24[0])
    t0 = fp2_add(t0,t1)
    q[1] = fp2_mul(t0,t2)

    return (q[0],q[1])


def mult_scalar_point(point, scalar,A24):
    x0 = point
    x1 = double_point(x0,A24)
    int_0 = 0
    int_1 = 1
    for i in range(177,-1,-1):
        k = (scalar >> i) & 1
        print(f"k: {k}") 
        if k == 0:
            x0_new = double_point(x0,A24)
            x1_new = add_point(x0,x1,point)
            int_0_new = 2*int_0
            int_1_new = int_0+int_1
        else:
            x0_new = add_point(x0,x1,point)
            x1_new = double_point(x1,A24)
            int_0_new = int_0+int_1
            int_1_new = 2*int_1
        int_0 = int_0_new
        int_1 = int_1_new
        x0 = x0_new
        x1 = x1_new
        x0[0].print_fp2()
        x0[1].print_fp2()
    print(int_0)
    print(((prime()+1)>>75))
    return x0


def xMULv2(point, scalar, A24):
    R0 = (fp2_t(fiat_p1913_set_one(),0),fp2_t(0,0))
    R1 = point
    bit = 0
    prevbit = 0
    for i in range(178,-1,-1):
        bit = (scalar >> i) & 1
        swap = bit ^ prevbit
        prevbit = bit
        mask = (1 << 64) - swap
        if swap != 0:
            aux = R0
            R0 = R1
            R1 = aux
        R0, R1 = xDBLADD(R0,R1,point,A24)
    swap = 0 ^ prevbit
    mask = (1 << 64) - swap
    if swap != 0:
        aux = R0
        R0 = R1
        R1 = aux
    return R0


def xDBLADD(P,Q,PQ,A24):
    t0 = fp2_add(P[0],P[1])
    t1 = fp2_sub(P[0],P[1])
    rx = fp2_sqr(t0)
    t2 = fp2_sub(Q[0],Q[1])
    sx = fp2_add(Q[0],Q[1])
    t0 = fp2_mul(t0,t2)
    rz = fp2_sqr(t1)
    t1 = fp2_mul(t1,sx)
    t2 = fp2_sub(rx,rz)
    rz = fp2_mul(rz,A24[1])
    rx = fp2_mul(rx,rz)
    sx = fp2_mul(A24[0],t2)
    sz = fp2_sub(t0,t1)
    rz = fp2_add(rz,sx)
    sx = fp2_add(t0,t1)
    rz = fp2_mul(rz,t2)
    sz = fp2_sqr(sz)
    sx = fp2_sqr(sx)
    sz = fp2_mul(sz,PQ[0])
    sx = fp2_mul(sx,PQ[1])

    return [(rx,rz),(sx,sz)]

