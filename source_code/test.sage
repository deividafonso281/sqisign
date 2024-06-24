from sage.all import *
from verify_signature import verify_signature
from sqisign_parameters import *
from aux import *
from fp2 import *
from fp import *

public_key_bytes = 64
NWORDS_FIELD = 4


class TestCase:
	def __init__(self,count,seed,mlen,msg,pk,sk,smlen,sm):
		self.count = count
		self.seed = seed
		self.mlen = mlen
		self.msg = msg
		self.pk = pk
		self.sk = sk
		self.smlen = smlen
		self.sm = sm

	def print_content(self):
		print(f"count = {self.count}\n seed = {self.seed}\n mlen = {self.mlen}\n msg = {self.msg}\n pk = {self.pk}\n sk = {self.sk}\n smlen = {self.smlen}\n sm = {self.sm}\n")

	def pk_hex_to_complex(self):
		hex_s = self.pk
		hex_real = hex_s[0:public_key_bytes]
		hex_imaginary = hex_s[public_key_bytes:2*public_key_bytes]
		hex_real = swap_numb(hex_real,public_key_bytes)
		int_real = int(hex_real,16)
		real_mont = fiat_p1913_to_montgomery(int_real)
		hex_imaginary = swap_numb(hex_imaginary,public_key_bytes)
		int_imaginary = int(hex_imaginary,16)
		imaginary_mont = fiat_p1913_to_montgomery(int_imaginary)
		c_coef = fiat_p1913_set_one()
		#print_word(real_mont)
		#print_word(imaginary_mont)
		#print_word(c_coef)
		self.pk = (fp2_t(real_mont,imaginary_mont),fp2_t(c_coef,0))


test_cases_file = open("../test_cases/PQCsignKAT_782_lvl1.rsp","r")

test_cases_raw = test_cases_file.read()

test_cases_file.close()

test_cases_text = test_cases_raw.split("\n\n")

test_cases_obj = []

for i in range(1,2):#len(test_cases_text)-1):
	test_case = test_cases_text[i].split("\n")
	count = test_case[0].split(" ")
	seed = test_case[1].split(" ")
	mlen = test_case[2].split(" ")
	msg = test_case[3].split(" ")
	pk = test_case[4].split(" ")
	sk = test_case[5].split(" ")
	smlen = test_case[6].split(" ")
	sm = test_case[7].split(" ")
	test_cases_obj.append(TestCase(int(count[2]),seed[2],int(mlen[2]),msg[2],pk[2],sk[2],int(smlen[2]),sm[2]))
	test_cases_obj[-1].pk_hex_to_complex()
	
verify_signature(test_cases_obj[0].sm,test_cases_obj[0].pk,test_cases_obj[0].msg)
