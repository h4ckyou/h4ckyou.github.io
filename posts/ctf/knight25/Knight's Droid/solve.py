def decrypt(ciphertext, key):
    plaintext = ""
    for char in ciphertext:
        if char.isalpha():
            offset = 65 if char.isupper() else 97
            plaintext += chr((ord(char) - offset - key) % 26 + offset)
        else:
            plaintext += char  
    return plaintext


enc = "GYPB{_ykjcnwp5_GJECDP_u0q_c0p_uKqN_Gj1cd7_zN01z_}"

for key in range(0, 26):
    res = shift_cipher_decrypt(enc, key)
    if "KCTF" in res:
        print(res)
