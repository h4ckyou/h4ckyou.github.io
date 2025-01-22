from string import punctuation, ascii_letters, digits
import gdb

def extract_values(reg):
    values = []
    reg = reg.splitlines()
    for i in range(len(reg)):
        x = reg[i].split(":")[-1].strip().split()
        as_int = list(map(int, x))
        values.extend(as_int)
    return values

gdb.execute("aslr off")
gdb.execute("b *0x555555555d73")
flag = ""
cnt = 0
charset = punctuation + ascii_letters + digits

while cnt < 34:
    for i in charset:
        tmp = flag + (i * (34 - cnt))
        with open("f.txt", "w") as f:
            f.write(tmp)
        gdb.execute(f"r < f.txt")

        rsi = gdb.execute("x/34ub $rsi", to_string=True)
        rdi = gdb.execute("x/34ub $rdi", to_string=True)
        rsi = extract_values(rsi)
        rdi = extract_values(rdi)

        if rsi[cnt] == rdi[cnt]:
            flag += i
            cnt += 1
            print(f"{flag = }")
            break
        print(f"{flag = }")

    print(f"{flag = }")
