from pwn import *

a = ELF("./They-are-many", checksec=False)

hm = a.sym
funcs = []

for key, val in hm.items():
    if len(key) == 20 and '_' not in key:
        funcs.append(key)
    
with open('func.txt', 'w') as f:
    for func in funcs:
        f.write(func)
        f.write('\n')
    
