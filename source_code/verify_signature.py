from sage.all import *
from sqisign_parameters import *
from aux import *
from fp2 import *
from fp import *
from ec import *

SIGNATURE_SIZE = 177
ZIP_SIZE = 141
R_SIZE = 17
S1_SIZE = 10
S2_SIZE = 8


class CompressedIsogeny:
    # Comments for future David: as of June 21st I am not sure about s order, maybe need to swap s[i] with s[size-i] later
    def __init__(self,bitearray):
        self.b = bitearray[2*ZIP_SIZE-2:2*ZIP_SIZE]
        self.s = []
        for i in range(14):
            start = 20*i
            hex_s = swap_numb(bitearray[start:start+20],20)
            byte_s = bytearray.fromhex(hex_s)
            int_s = int.from_bytes(byte_s,signed=True)
            self.s.append(int_s)


    def print_comp(self):
        print(self.b)
        print(self.s)


class Signature:
    def __init__(self,comp_isog,r,s,msg):
        self.comp_isog = comp_isog
        self.r = r
        self.s = s
        self.msg = msg


def complete_basis(curve, point, xcord=1):
    print(curve.a2())
    print(point.xy())
    #while True:
    #    x = x + im_unity
    #    if curve_.is_x_coord(xcord):
    #        xcordrs = 



def torsion_basis(curve):

    twoc = fp2_add(curve[1],curve[1])
    A24 = (fp2_add(curve[0],twoc),fp2_add(twoc,twoc))

    xcord = fp2_t(fiat_p1913_set_one(),0)
    found = 0

    while found == 0:
        counter = 0
        xcord = fp2_add(xcord,fp2_t(0,fiat_p1913_set_one()))
        c2 = fp2_sqr(curve[1])
        t0 = fp2_mul(xcord,c2)
        t2 = fp2_add(t0,fp2_mul(curve[0],curve[1]))
        t3 = fp2_mul(t2,xcord)
        t1 = fp2_mul(fp2_add(t3,c2),xcord)
        if fp2_is_square(t1):
            point = (xcord,fp2_t(fiat_p1913_set_one(),0))
            point = xMULv2(point,p_cofactor_for_2f,A24)
            d_point = point
            for i in range(74):
                d_point = double_point(d_point, A24)
            if d_point[1].re != 0 and d_point[1].im != 0:
                found = 1
    
    found = 0
    while found == 0:
        xcord = fp2_add(xcord,fp2_t(0,fiat_p1913_set_one()))

        t0 = fp2_mul(xcord,c2)
        t2 = fp2_add(t0,fp2_mul(curve[0],curve[1]))
        t3 = fp2_mul(t2,xcord)
        t1 = fp2_mul(fp2_add(t3,c2),xcord)
        if fp2_is_square(t1):
            point2 = (xcord, fp2_t(fiat_p1913_set_one(),0))
            point2 = xMULv2(point2,p_cofactor_for_2f,A24)
            d_point2 = point2
            for i in range(74):
                d_point2 = double_point(d_point2,A24)
            if d_point[1].re != 0 and d_point[1].im != 0:
                if is_point_equal(point,point2) == False:
                    found = 1
    point2[0].print_fp2()
    point2[1].print_fp2()
    return 0


def signature_decode(signature):
    zip_size = 2*ZIP_SIZE
    zip_bitearray = signature[:zip_size]
    zip_obj = CompressedIsogeny(zip_bitearray)

    r_size = 2*R_SIZE
    r_bitearray = signature[zip_size:zip_size+r_size]
    r_bitearray = swap_numb(r_bitearray,r_size)
    int_r = int(r_bitearray,16)
    
    s_size = 2*(S1_SIZE+S2_SIZE+1)
    s_bitearray = signature[zip_size+r_size:zip_size+r_size+s_size]
    s_obj = [s_bitearray[:2],s_bitearray[2:2*S1_SIZE+2],s_bitearray[2*S1_SIZE+2:2*S1_SIZE+2*S2_SIZE+2]]
    s_obj[0] = int(s_obj[0],16) 
    s_obj[1] = int(swap_numb(s_obj[1],2*S1_SIZE),16)
    s_obj[2] = int(swap_numb(s_obj[2],2*S2_SIZE),16)
    msg = signature[zip_size+r_size+s_size:]


    #print(f"zip")
    #zip_obj.print_comp()
    #print(f"r: {int_r} \n s: {s_obj}")

    return Signature(zip_obj,int_r,s_obj,msg)
    
    


def verify_signature(signature, public_key, message):
	
    signature = signature_decode(signature)
    torsion_basis(public_key)


