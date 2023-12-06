from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
import zlib

wordlist = "/usr/share/wordlists/rockyou.txt"

with open("flag.zip", "rb") as fp:
    file = fp.read()

salt = file[0:16]
iv = file[16:32]
ct = file[32:]

try:
    with open(wordlist, encoding="latin-1") as file:
        for line in file:
            if line.isprintable:
                password = line.strip()
               # print(f"Trying password: {password}")
                key = PBKDF2(password, salt, dkLen=32, count=1000000)
                cipher = AES.new(key, AES.MODE_CBC, iv)
                dec = cipher.decrypt(ct)

                try:
                    zip_file = zlib.decompress(dec)
                    print(f"[Password: {password}]")
                    print(zip_file)
                    exit(0)
                except zlib.error:
                    pass
            else:
                pass
except Exception as e:
    print(e)
