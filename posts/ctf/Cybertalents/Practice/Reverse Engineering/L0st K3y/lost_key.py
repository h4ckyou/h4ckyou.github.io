def enc(st,key):
  dat=''
  for i in range(len(st)):
    dat+=chr(ord(st[i])^ord(key[i%len(key)]))
  return dat

key=[Removed]
flag=[Removed]

encrypted_flag=enc(flag,key)
print(''.join(['%02x'%ord(i) for i in encrypted_flag]))