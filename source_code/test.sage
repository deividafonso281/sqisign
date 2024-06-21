from sage.all import *
from verify_signature import verify_signature
from finite_field import *
from sqisign_parameters import *
from aux import *

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

	def swap_digits(self,key_part):
		array = [0 for i in range(public_key_bytes)]
		word_size = public_key_bytes//NWORDS_FIELD
		for i in range(NWORDS_FIELD):
			start = i*word_size
			end = (i+1)*word_size
			for j in range(0,word_size,2):
				array[start+j] = key_part[end-2-j]
				array[start+j+1] = key_part[end-1-j]
				array[end-2-j] = key_part[start+j]
				array[end-1-j] = key_part[start+j+1]
		key_part = ''.join(array)
		return key_part

	def fiat_p1913_to_montgomery(self,key_part):
		x4 = int(key_part[0:16],16)
		x1 = int(key_part[16:32],16)
		x2 = int(key_part[32:48],16)
		x3 = int(key_part[48:64],16)
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
	
	def fiat_p1913_set_one(self):
		
		#return int("46b4d86db2abae00031655e69e2fe2f232c75875e51a899cf",16)
		return int("2c75875e51a899cf31655e69e2fe2f236b4d86db2abae0000000000000000004",16)

	def print_content(self):
		print(f"count = {self.count}\n seed = {self.seed}\n mlen = {self.mlen}\n msg = {self.msg}\n pk = {self.pk}\n sk = {self.sk}\n smlen = {self.smlen}\n sm = {self.sm}\n")

	def pk_hex_to_complex(self):
		hex_s = self.pk
		hex_real = hex_s[0:public_key_bytes]
		hex_imaginary = hex_s[public_key_bytes:2*public_key_bytes]
		hex_real = self.swap_digits(hex_real)
		real_mont = self.fiat_p1913_to_montgomery(hex_real)
		hex_imaginary = self.swap_digits(hex_imaginary)
		imaginary_mont = self.fiat_p1913_to_montgomery(hex_imaginary)
		c_coef = self.fiat_p1913_set_one()
		print_word(real_mont)
		print_word(imaginary_mont)
		print_word(c_coef)
		self.pk = ((real_mont,imaginary_mont),(c_coef,0))


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
