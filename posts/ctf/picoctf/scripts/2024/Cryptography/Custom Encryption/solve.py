def generator(g, x, p):
    return pow(g, x) % p

def decrypt(cipher, shared_key):
    semi_cipher =  ""
    for value in cipher:
        semi_cipher += chr(value // (shared_key * 311))

    return semi_cipher

def xor_pwn(enc, key):
    pt = ""
    k_len = len(key)

    for idx, val in enumerate(enc):
        k_chr = key[idx % k_len]
        d_chr = chr(ord(k_chr) ^ ord(val))
        pt += d_chr
    
    print(pt[::-1])

a, b = 89, 27
p, g = 97, 31

u = generator(g, a, p)
v = generator(g, b, p)
key = generator(v, a, p)
b_key = generator(u, b, p)

assert key == b_key
shared_key = key

cipher = [33588, 276168, 261240, 302292, 343344, 328416, 242580, 85836, 82104, 156744, 0, 309756, 78372, 18660, 253776, 0, 82104, 320952, 3732, 231384, 89568, 100764, 22392, 22392, 63444, 22392, 97032, 190332, 119424, 182868, 97032, 26124, 44784, 63444]
semi_cipher = decrypt(cipher, shared_key)
flag = xor_pwn(semi_cipher, "trudeau")
