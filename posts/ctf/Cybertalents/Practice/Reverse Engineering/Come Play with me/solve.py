"""
Python compiled binary

To unpack:
- objcopy --dump-section pydata=pydata.dump come-play-withme
- python3 ~/Desktop/Tools/pyinstxtractor-ng/pyinstxtractor-ng.py pydata.dump

We get python bytecode in the extracted directory

Decompile using pycdc to get original python code

The result is an obfuscated code

Manually read it and deobfuscated it

Four functions given?
- help --> print help menu
- new --> seed with current time
- next --> want's us to predict the next random() value
- flag --> hidden function (gives us flag?)

From reading the code our goal is to use the flag function to get the flag (obviously!)

But for that we need the sum of the given name to be the right value because it uses that multiplied by 4 for the DES key

https://pycryptodome.readthedocs.io/en/latest/src/cipher/des.html

It must be of length 8 so (10-99)?

- Since the operation done on the sum of name is {(name % 225) + 95} , if i give it a name whose sum is 5 the result is going to be 100
- We can then use the "new" function to seed with the current time 
- Then we use the "next" function to predict the next number and doing that it would subtract our sum_name with 1 making it 99
- Then we try use the "flag" function to decrypt the flag
- If it's the right sum_name we would get the flag but if it isn't we would not get it
- Repeat the steps till sum_name equals 10, during the process we should get the right key value and get the flag

*******************
Guys fr i got stucked for a long time here (1hour+) debugging

- Python2.7 and Python3.11 random module works differently even when seeded the same way god dammit!

*******************

An easier way to solve this is to just call the decode_unicode function on the encrypted flag then just brute force the key 

I didn't do it that way because for some reason python was giving me a "none" printable string so i went ahead with this my approach!
"""

from pwn import process, context
import random
import time
import base64
import subprocess


def rand_list(cx, ct):
    cmd = f'python2.7 generate.py {cx} {ct}'
    execute = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output, err = execute.communicate()
    r = output.split()
    
    return r


io = process("./come-play-withme")
context.log_level = 'info'

function = [b'new', b'next', b'flag']
name = b'\x05'
output = []

io.recvuntil(b"name:")
io.sendline(name)

io.sendline(function[0])

io.sendline(function[1])
io.recvline()
io.recvuntil(b"Current is ")
cx = int(io.recvline().split()[0])
ct = int(time.time())

# print(f'current time(): {ct}')
# print(f'current randint(): {cx}')

random_list = rand_list(cx, ct)
n = 183 # -> really just the range i just want to stop at going above makes DES scream

io.sendline(b'1337') # -> junkk

for idx in range(3, n, 2):
    io.sendline(function[1])
    io.sendline(str(random_list[idx]).encode())
    io.sendline(function[2])
    io.recvlines(2)
    enc = io.recvline().split()[-1]
    output.append(enc)


for i in output:
    r = base64.b64decode(i)
    if b"flag" in r:
        print(f'Flag: {r.decode()}')
        break


io.close()
