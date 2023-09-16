def canConstruct(ransomNote, magazine):
    magazine_table = {}
    ransom_table = {}
    tt = []

    for i in ransomNote:
        if i in ransom_table:
            ransom_table[i] += 1
        else:
            ransom_table[i] = 1
    
    for i in magazine:
        if i in magazine_table:
            magazine_table[i] += 1
        else:
            magazine_table[i] = 1

    for keyR, valueR in ransom_table.items():
        if keyR in magazine_table and magazine_table[keyR] >= valueR:
            tt.append(True)
        else:
            tt.append(False)
    
    if False in tt:
        return False
    else:
        return True

ransomNote = "fihjjjjei"
magazine = "hjibagacbhadfaefdjaeaebgi"
r = canConstruct(ransomNote, magazine)

print(r)
