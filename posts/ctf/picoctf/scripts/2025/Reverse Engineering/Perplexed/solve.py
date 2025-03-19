import gdb
import string
import ctypes


gdb.execute(f"b *0x40123E")

charset = string.printable
flag = ""

while len(flag) != 0x1b:
    for j in charset:
        guess = (flag + j).encode()
        guess = guess.ljust(0x1b, b".")

        with open("_cracking", "wb") as f:
            f.write(guess)

        gdb.execute("r < _cracking")

        for i in range((len(flag) * 7)):
            gdb.execute("c")
            print(i)

        count = 0
        for i in range(8):
            try:
                al = int(gdb.parse_and_eval("$al"))
                gdb.execute("c")
                count += 1
            except Exception:
                pass

        if count == 8:
            flag += j
            print(f"found: {guess}")
            print(f"Current flag: {flag}")
            break
        else:
            print(f"count: {count}")
