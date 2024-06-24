from sage.all import *
from finite_field import *
from sqisign_parameters import *
from aux import *

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

    A24 = (curve[0]+fp2_mul(2+0*im_unity,curve[1]),fp2_mul(4+0*im_unity,curve[1]))

    xcord = fiat_p1913_set_one()  + 0*im_unity
    found = 0

    while found == 0:
        counter = 0
        xcord = xcord + fiat_p1913_set_one()*im_unity
        c2 = fp2_sqr(curve[1])
        t1 = fp2_mul((fp2_mul((fp2_mul(xcord,c2)+fp2_mul(curve[0],curve[1])),xcord)+c2),xcord)
        if fp2_is_square(t1):
            point = (xcord,fiat_p1913_set_one()+0*im_unity)
            point = mult_scalar_point(point,p_cofactor_for_2f,A24)
            print_word(re(point[0]))
            print_word(im(point[0]))
            d_point = point 
            while counter < 75 and d_point[1] != 0:
                counter = counter + 1
                d_point = double_point(d_point, A24)
            if counter == 75:
                found = 1
    
    #print("xcord point")
    #print_word(re(point[0]))
    #print_word(im(point[0]))
    #print("zcord point")
    #print_word(re(point[1]))
    #print_word(im(point[1]))
    #complete_basis(curve,basis1,xcord)

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


