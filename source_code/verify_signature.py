from sage.all import *

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


    print(f"zip")
    zip_obj.print_comp()
    print(f"r: {int_r} \n s: {s_obj}")

    return Signature(zip_obj,int_r,s_obj,msg)
    
    


def verify_signature(signature, public_key, message):
	signature = signature_decode(signature)
