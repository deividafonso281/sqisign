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
    def __init__(self,bitearray):
        self.b = bitearray[:2]
        self.s = []
        for i in range(14):
            start = 2+20*i
            byte_s = bytearray.fromhex(bitearray[start:start+20])
            int_s = int.from_bytes(byte_s,byteorder='little',signed=False)
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

    xcord = 1
    found = 0
    counter = 0
    curve = curve.montgomery_model()
    while found == 0:
        counter = counter + 1
        xcord = xcord + im_unity
        if curve.is_x_coord(xcord):
            divisor = 2
            i = 1
            curve_point = curve.lift_x(xcord)
            basis1 = ((prime()+1)//(2**f))*curve_point
            while i < f:
                multiple = basis1*divisor
                print(multiple[0])
                if multiple[0] == 0:
                    if multiple[1] == 1 and multiple[2] == 0:
                        break
                divisor = divisor * 2
                i = i+1
            print(log(divisor,2))
            if multiple[0] == 0:
                found = 1
                print(counter)
                print(basis1*divisor)
    complete_basis(curve,basis1,xcord)

    return 0


def signature_decode(signature):
    zip_size = 2*ZIP_SIZE
    zip_bitearray = signature[:zip_size]
    zip_obj = CompressedIsogeny(zip_bitearray)

    r_size = 2*R_SIZE
    r_bitearray = signature[zip_size:zip_size+r_size]
    bytes_r = bytearray.fromhex(r_bitearray)
    int_r = int.from_bytes(bytes_r,byteorder='little',signed=False)
    
    s_size = 2*(S1_SIZE+S2_SIZE+1)
    s_bitearray = signature[zip_size+r_size:zip_size+r_size+s_size]
    s_obj = [s_bitearray[:2],s_bitearray[2:2*S1_SIZE+2],s_bitearray[2*S1_SIZE+2:2*S1_SIZE+2*S2_SIZE+2]]
    for i in range(len(s_obj)):
        bytes_el = bytearray.fromhex(s_obj[i])
        int_el = int.from_bytes(bytes_el,byteorder='little',signed=False)
        s_obj[i] = int_el

    msg = signature[zip_size+r_size+s_size:]


    #print(f"zip")
    #zip_obj.print_comp()
    #print(f"r: {int_r} \n s: {s_obj}")

    return Signature(zip_obj,int_r,s_obj,msg)
    
    


def verify_signature(signature, public_key, message):
	
    signature = signature_decode(signature)
    #torsion_basis(public_key)


