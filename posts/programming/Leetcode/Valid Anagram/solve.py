def isAnagram(s, t):
    if len(s) != len(t):
        return False

    htS = {}
    htT = {}

    for i in s:
        if i in htS:
            htS[i] += 1
        else:
            htS[i] = 1

    for j in t:
        if j in htT:
            htT[j] += 1
        else:
            htT[j] = 1
        
    
    for keyT, valueT in htT.items():
        if keyT not in htS:
            return False

    for keyS, valueS in htS.items():
        if htT[keyS] != valueS:
            return False
    
    return True
    
s = "aacc"
t = "ccac"

r = isAnagram(s, t)
print(r)
