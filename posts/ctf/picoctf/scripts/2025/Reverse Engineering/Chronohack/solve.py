import random
from pwn import process, remote
import time


def get_random(length, tim):
    alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    random.seed(tim)  # seeding with current time
    s = ""
    for i in range(length):
        s += random.choice(alphabet)
    return s


#proc = process(["python3", "token_generator.py"])
proc = remote("verbal-sleep.picoctf.net", 52131)
act = int(time.time() * 1000)
print(proc.recv())
for i in range(act-150, act+150):
        proc.sendline(get_random(20, i).encode('utf-8'))
        response = proc.recv()
        print(response)
        if b"Sorry, your token does not match." not in response:
                print(response)
                break 
