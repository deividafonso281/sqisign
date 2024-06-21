from sage.all import *

reset()

parameters_file = open("../parameters/sqisign_parameters.txt","r")

parameters_raw = parameters_file.read()

parameters_file.close()

parameters_text = parameters_raw.split("\n")

p = int((parameters_text[1].split(' '))[2],16)
B = int((parameters_text[2].split(' '))[2])

mont = int("d72e7d67c30cd3d30a841ab0920655d20afd6c1025a1c2e233625ae400674d4",16)

f = 75

def prime():
    return p


def B_func():
    return B

def montgomery():
    return mont
