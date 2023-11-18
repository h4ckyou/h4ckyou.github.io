from z3 import *

flag_bytes = [BitVec(f"f_{i}", 8) for i in range(22)]

s = Solver()
s.add(flag_bytes[18] * flag_bytes[7] & flag_bytes[12] ^ flag_bytes[2] == 36)
s.add(flag_bytes[1] % flag_bytes[14] - flag_bytes[21] % flag_bytes[15] == -3)
s.add(flag_bytes[18] * flag_bytes[7] & flag_bytes[12] ^ flag_bytes[2] == 36)
s.add(flag_bytes[1] % flag_bytes[14] - flag_bytes[21] % flag_bytes[15] == -3)
s.add(flag_bytes[10] + flag_bytes[4] * flag_bytes[11] - flag_bytes[20] == 5141) 
s.add(flag_bytes[19] + flag_bytes[12] * flag_bytes[0] ^ flag_bytes[16] == 8332 )
s.add(flag_bytes[9] ^ flag_bytes[13] * flag_bytes[8] & flag_bytes[16] == 113)
s.add(flag_bytes[3] * flag_bytes[17] + flag_bytes[5] + flag_bytes[6] == 7090)
s.add(flag_bytes[21] * flag_bytes[2] ^ flag_bytes[3] ^ flag_bytes[19] == 10521) 
s.add(flag_bytes[11] ^ flag_bytes[20] * flag_bytes[1] + flag_bytes[6] == 6787)
s.add(flag_bytes[7] + flag_bytes[5] - flag_bytes[18] & flag_bytes[9] == 96)
s.add(flag_bytes[12] * flag_bytes[8] - flag_bytes[10] + flag_bytes[4] == 8277) 
s.add(flag_bytes[16] ^ flag_bytes[17] * flag_bytes[13] + flag_bytes[14] == 4986)
s.add(flag_bytes[0] * flag_bytes[15] + flag_bytes[3] == 7008)
s.add(flag_bytes[13] + flag_bytes[18] * flag_bytes[2] & flag_bytes[5] ^ flag_bytes[10] == 118)
s.add(flag_bytes[0] % flag_bytes[12] - flag_bytes[19] % flag_bytes[7] == 73)
s.add(flag_bytes[14] + flag_bytes[21] * flag_bytes[16] - flag_bytes[8] == 11228) 
s.add(flag_bytes[3] + flag_bytes[17] * flag_bytes[9] ^ flag_bytes[11] == 11686)
s.add(flag_bytes[15] ^ flag_bytes[4] * flag_bytes[20] & flag_bytes[1] == 95)
s.add(flag_bytes[6] * flag_bytes[12] + flag_bytes[19] + flag_bytes[2] == 8490) 
s.add(flag_bytes[7] * flag_bytes[5] ^ flag_bytes[10] ^ flag_bytes[0] == 6869)
s.add(flag_bytes[21] ^ flag_bytes[13] * flag_bytes[15] + flag_bytes[11] == 4936) 
s.add(flag_bytes[16] + flag_bytes[20] - flag_bytes[3] & flag_bytes[9] == 104)
s.add(flag_bytes[18] * flag_bytes[1] - flag_bytes[4] + flag_bytes[14] == 5440)
s.add(flag_bytes[8] ^ flag_bytes[6] * flag_bytes[17] + flag_bytes[12] == 7104)
s.add(flag_bytes[11] * flag_bytes[2] + flag_bytes[15] == 6143)

byte = []
if s.check() == sat:
    m = s.model()
    for i in range(22):
        byte.append(chr(m.eval(flag_bytes[i]).as_long()))
    
print(''.join(byt
