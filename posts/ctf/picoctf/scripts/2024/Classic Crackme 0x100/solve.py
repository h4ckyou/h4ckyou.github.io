from z3 import *

output = "mpknnphjngbhgzydttvkahppevhkmpwgdzxsykkokriepfnrdm"
secret1 = 85
secret2 = 51
secret3 = 15
fix = 97
i = 0

s = Solver()

arr = [BitVec(f'f_{i}', 8) for i in range(len(output))]
tmp = [BitVec(f'f_{i}', 8) for i in range(len(output))]

for v in arr:
    s.add(v > 0x60)
    s.add(v < 0x7f)
          
while i < 3:
    for j in range(len(output)):
        random1 = ((secret1 & (j % 255)) + (secret1 & ((j % 255) >> 1))) 
        random2 = ((random1 & secret2) + (secret2 & (random1 >> 2))) 
        val = (((random2 & secret3) + arr[j] - fix + (secret3 & (random2 >> 4))) % 26 + fix) 
        arr[j] = val

    i += 1

for j in range(len(output)):
    s.add(arr[j] == ord(output[j]))

if s.check() == sat:
    m = s.model()
    inp = ""

    for i in tmp:
        inp += chr(m[i].as_long())
    
    print(inp)
