from sage.all import *
from verify_signature import verify_signature

public_key_bytes = 64

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
		i = ComplexField(prec=public_key_bytes)
		hex = self.pk
		real = bytearray.fromhex(hex[0:public_key_bytes//2])
		real = int.from_bytes(real,byteorder='little')
		imaginary = bytearray.fromhex(hex[public_key_bytes//2:public_key_bytes])
		imaginary = int.from_bytes(imaginary,byteorder='little')
		self.pk = i(real,imaginary)
			


test_cases_file = open("../test_cases/PQCsignKAT_782_lvl1.rsp","r")

test_cases_raw = test_cases_file.read()

test_cases_file.close()

test_cases_text = test_cases_raw.split("\n\n")

test_cases_obj = []

for i in range(1,len(test_cases_text)-1):
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
