from pwn import *
from warnings import filterwarnings
filterwarnings("ignore")

enc_flag = b'\x16\x13\x05\r\x0b\x0f\x11\x00RHz\x03}oD\x02\x0f\x12\x04\x11>\x04QG\x03A^D\x01hR\x04#)$\x1ch'
known_pt = "A"*30

with open("flag.txt", "w") as fp:
    fp.write(known_pt)

io = process("./sugarplum")
io.close()

with open("enc", "rb") as fp:
    enc_pt = fp.read()

key = xor(known_pt, enc_pt)

flag = xor(enc_flag, key)
print(flag)
