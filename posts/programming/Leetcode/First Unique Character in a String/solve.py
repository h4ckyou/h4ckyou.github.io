def firstUniqChar(s):
    ht = {}

    for i in s:
        if i in ht:
            ht[i] += 1
        else:
            ht[i] = 1
    
    for key, value in ht.items():
        if value == 1:
            return s.index(key)
        
    return -1

s = "loveleetcode"
r = firstUniqChar(s)
print(r)
