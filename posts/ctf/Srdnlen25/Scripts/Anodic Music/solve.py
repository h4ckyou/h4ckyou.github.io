from hashlib import md5
from string import printable

def dfs(current_flag):
    if len(current_flag) == 62:
        print(current_flag)
        return 

    for char in printable:
        trial = current_flag + char
        if md5(trial.encode()).hexdigest() not in hash_map.keys():
            dfs(current_flag + char)


with open("hardcore.bnk", "rb") as f:
    hashes = bytearray(f.read())

hash_map = {}

for i in range(0,len(hashes),16):
    hash_map[hashes[i:i+16].hex()] = True

dfs("srdnlen{")
