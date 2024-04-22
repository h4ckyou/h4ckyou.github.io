import string
from z3 import *

def shift2(char, key):
    tmp = ord(char)
    r = ""
    if (tmp > 0x20) and (tmp <= 0x7E):
        tmp += key
        if tmp <= 0x7E:
            shift = 0x0
        else:
            shift = 0x5e
        r = chr(tmp - shift)
    else:
        r = chr(tmp)

    return r

def shift1(char):
    tmp = ord(char)
    r = ""
    if (tmp > 0x40) and (tmp <= 0x5b):
        tmp -= 0xd
        if (tmp > 0x40):
            shift = 0x0
        else:
            shift = 0x1a
        r = chr(tmp + shift)
    
    elif (tmp > 0x60) and (tmp <= 0x7b):
        tmp -= 0xd
        if (tmp > 0x60):
            shift = 0x0
        else:
            shift = 0x1a
        r = chr(tmp + shift)
    else:
        r = chr(tmp)

    return r

def phase3():
    r = ""
    charset = string.printable
    expected = [ 0x39, 0x5a, 0x79, 0x45, 0x45, 0x6d, 0x58, 0x24, 0x56, 0x4a, 0x3b, 0x27, 0x79, 0x58, 0x24, 0x26, 0x56, 0x38, 0x65, 0x7b, 0x56, 0x4a, 0x5a, 0x4c, 0x58]

    for i in range(len(expected)):
        for char in charset:
            a = shift2(char, 45)
            b = shift1(a)
            c = shift2(b, 18)
            d = shift1(c)
            e = shift2(d, 22)
    
            if (ord(e) == expected[i]):
                # print([char, e, chr(expected[i])])
                r += char
                break
            
    print(r)

    phase3 = "DawgCTF{5p1NNinG_S7t1nGs_4a3_SpUn}"
    print(phase3)


def phase4():
    array = [0xe6, 0x24, 0x00, 0x00, 0x60, 0x24, 0x00, 0x00, 0xd3, 0x24, 0x00, 0x00, 0x62, 0x24, 0x00, 0x00, 0x5f, 0x00, 0x00, 0x00, 0xd1, 0x24, 0x00, 0x00, 0xde, 0x24, 0x00, 0x00, 0x60, 0x24, 0x00, 0x00, 0x5f, 0x00, 0x00, 0x00, 0xe4, 0x24, 0x00, 0x00, 0xdd, 0x24, 0x00, 0x00, 0x60, 0x24, 0x00, 0x00, 0xd2, 0x24, 0x00, 0x00, 0xea, 0x24, 0x00, 0x00, 0xd3, 0x24, 0x00, 0x00, 0xd4, 0x24, 0x00, 0x00, 0x5f, 0x00, 0x00, 0x00, 0xe2, 0x24, 0x00, 0x00, 0x66, 0x24, 0x00, 0x00, 0xe1, 0x24, 0x00, 0x00, 0x60, 0x24, 0x00, 0x00, 0xdd, 0x24, 0x00, 0x00, 0xd6, 0x24, 0x00, 0x00]
    expected = []

    for i in range(0, len(array), 4):
        n1 = array[i:i+4]
        n2 = n1[::-1]
        sum = "0x"
        for val in n2:
            sum += hex(val)[2:]

        expected.append(int(sum, 16))


    charset = string.printable
    res = ""

    for j in range(len(expected)):
        for i in range(len(charset)):
            value = ord(charset[i])

            if (value < 0x61) or (value > 0x7a):
                if (value < 0x31) or (value > 0x39):
                    if value == 0x30:
                        r = value + 0x24ba
                else:
                    r = value + 0x242f
            else:
                r = value + 0x246f

            print([charset[i], r, expected[j]])
            if r == expected[j]:
                res += charset[i]
                break
        
    print(res)
    res = "DawgCTF{w1d3_bo1_un1c0de_s7r1ng}"
    print(res)


def phase5():
    """
    rbp-0x36 = ((val >> 0x4) << 0x2) & 0xc | (val >> 0x4) >> 0x2
    rbp-0x35 = ((val & 0xf) << 0x2) & 0xc | (val & 0xf) >> 0x2

    edx = (val >> 0x4) >> 0x2
    eax = (val & 0xf) << 0x2) & 0xc
    edx = (val & 0xf) >> 0x2

    esi = (((val & 0xf) << 0x2) & 0xc | (val & 0xf) >> 0x2) << 0x4
    ecx = rbp-0x36

    r = (esi | ecx) & 0xff
    val[i] = r
    """
    buf = [-63, 93, -36, -11, 121, 101, -11, 92, 21, -115, 76, -79, -39, -11, 105, -79, -36, 12, -11, 5, 97, -52, -55, -52, -51]
    buf = [i & 0xff for i in buf]

    valid = [BitVec(f"f_{i}", 64) for i in range(len(buf))]
    tmp = valid
    s = Solver()

    for i in range(len(valid)):
        s.add(((((((valid[i] & 0xf) << 0x2) & 0xc | (valid[i] & 0xf) >> 0x2) << 0x4) | (((valid[i] >> 0x4) << 0x2) & 0xc | (valid[i] >> 0x4) >> 0x2)) & 0xff) == buf[i])
    
    if s.check() == sat:
        m = s.model()
        r = ""
        for i in range(len(valid)):
            r += chr(m[valid[i]].as_long())
        else:
            print("not sat")

    print(r)
    r = "DawgCTF{Cu7_mY_5Tr1Ng_iN70_PI3c3s}"
    print(r)


def phase6():
    buf = [90, 106, 109, 106, 83, 61, 31, 5, 25, 105, 88, 57, 86, 92, 51, 12, 61, 107, 97, 100, 99, 98, 96, 22]
    valid = [BitVec(f"f_{i}", 64) for i in range(len(buf))]
    tmp = [BitVec(f"f_{i}", 64) for i in range(len(buf))]
    s = Solver()

    for i in range(len(valid)-1):
        valid[i] = valid[i] ^ valid[i+1] ^ 0x34

    valid[len(buf)-1] = valid[len(buf)-1] ^ 0x34

    j = 0
    while j < len(valid) >> 1:
        valid[j] = valid[j] ^ valid[(len(buf) - j) - 1]
        valid[(len(buf) - j) - 1] = valid[(len(buf) - j) - 1] ^ valid[j]
        valid[j] = valid[j] ^ valid[(len(buf) - j) - 1]
        j += 1
    
    for i in range(len(buf)):
        s.add(valid[i] == buf[i])

    if s.check() == sat:
        m = s.model()
        r = ""
        for i in range(len(valid)):
            r += chr(m[tmp[i]].as_long())
    else:
        print("not sat")
    
    # print(r)
    r = "DawgCTF{Ca5c4d1ng_X0R_3nCrYP7i0n}"
    print(r)


def main():
    phase3()
    phase4()
    phase5()
    phase6()

if __name__ == '__main__':
    main()
