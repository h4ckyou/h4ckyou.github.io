from Crypto.Cipher import AES
from pwn import xor
import itertools

def decrypt_flag(ct, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(ct)
    
    return decrypted

def recover_key(signature, iv):
    signature = bytes.fromhex(signature)
    iv = bytes.fromhex(iv)
    key = xor(signature, iv)[::-1]
 
    return key

# cipher = "888fb84744ea0ea84165cf6418b07bd829cc2a695e7d5bb4acdae1179bac51f02486993c80c028b3350029c171819ad9166b78e998c87be7233a302b83f0ebe67f4684682c4b3798f42587173965"
# signature = cipher[-32:]
# init_iv = cipher[0:28]
# ct = cipher[28:-32]
# full_iv = {1000-9999}+init_iv

def main():
    charset = '01234567890123456789abcdef'

    for combination in itertools.product(charset, repeat=4):
        init = ''.join(combination)
        signature = "ebe67f4684682c4b3798f42587173965"
        iv = f"{init}888fb84744ea0ea84165cf6418b0"
        ct = "7bd829cc2a695e7d5bb4acdae1179bac51f02486993c80c028b3350029c171819ad9166b78e998c87be7233a302b83f0"
        key = recover_key(signature, iv)

        IV = bytes.fromhex(iv)
        CT = bytes.fromhex(ct)
        pt = decrypt_flag(CT, key, IV)
        # print(pt)
        if b'urchinsec' in pt:
            print(pt)

if __name__ == '__main__':
    main()
