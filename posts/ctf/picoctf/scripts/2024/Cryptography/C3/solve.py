lookup1 = "\n \"#()*+/1:=[]abcdefghijklmnopqrstuvwxyz"
lookup2 = "ABCDEFGHIJKLMNOPQRSTabcdefghijklmnopqrst"

ciphertext = "DLSeGAGDgBNJDQJDCFSFnRBIDjgHoDFCFtHDgJpiHtGDmMAQFnRBJKkBAsTMrsPSDDnEFCFtIbEDtDCIbFCFtHTJDKerFldbFObFCFtLBFkBAAAPFnRBJGEkerFlcPgKkImHnIlATJDKbTbFOkdNnsgbnJRMFnRBNAFkBAAAbrcbTKAkOgFpOgFpOpkBAAAAAAAiClFGIPFnRBaKliCgClFGtIBAAAAAAAOgGEkImHnIl"

out = ""

prev = 0
for char in ciphertext:
    cur = lookup2.index(char)
    out += lookup1[(cur + prev) % 40]
    prev = (cur + prev) % 40

chars = out
b = 1 / 1

r = ""

for i in range(len(chars)):
    if i == b * b * b:
        r += chars[i] 
        b += 1 / 1

print(r) 
