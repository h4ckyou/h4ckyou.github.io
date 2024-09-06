"""
Opens up the selected file and reads in 256 bytes which is then stored in variable p

Does some string manipulation based on the substring of the value returned from calling hexStr on p (i'll look at the implementation soon)

Next it compares the concatenated manipulated string to variable b

If it matches then it prints out the flag!

Basically the flag is dependent on the content of the file we upload 

Since we need to upload a right file i checked if the binary had embedded files

And it did

binwalk --dd=".*" cloak.exe

The file 7F4428 is the expected file
"""

import os


def tohexStr(cnt):
    return ''.join(f'{ord(c):02x}' for c in cnt)


right = "FF0003060C1204121212000100C40307"
junk = '.' * 0x100
content = list('0x') + list(tohexStr(junk))
sub_idx = [2, 34, 66, 98, 130, 162, 194, 226, 258, 290, 322, 354, 386, 418, 450, 482]
pos = []


for i in sub_idx:
    pos.append(i)
    pos.append(i+1)

files = os.listdir()

for file in files:
    with open(file, 'rb') as f:
        hmm = f.read()
        if len(hmm):
            chk = hmm[0:500].decode('latin')
            r = '0x' + tohexStr(chk)
            # print(r[pos[0]] + r[pos[1]])
            if (r[pos[0]] + r[pos[1]] == 'ff') \
                  and (r[pos[2]] + r[pos[3]] == '00') \
                      and (r[pos[4]] + r[pos[5]] == '03') \
                        and (r[pos[6]] + r[pos[7]] == '06') \
                            and (r[pos[8]] + r[pos[9]] == '0c'):
                print(file)        
        f.close()

# for i in range(0, len(right), 2):
#     val = right[i:i+2]
#     # idx = pos[i:i+2]
#     # print(idx, pos[i], pos[i+1])
#     if i < len(pos) - 1: 
#         content[pos[i]] = val[0]
#         content[pos[i + 1]] = val[1]
#     else:
#         print('out of bound')

# done = ''.join(content)
# print(done)
# r = bytes.fromhex(done[2:])

# print(r)
# with open('my_file', 'wb') as f:
#     f.write(r)
#     f.close()


# print(len(r))
