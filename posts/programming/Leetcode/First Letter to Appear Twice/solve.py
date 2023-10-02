def repeatedCharacter(s):
    st = set()

    for char in s:
        if char in st:
            return char
        else:
            st.add(char)
    
    
s = "abccbaacz"
r = repeatedCharacter(s)

print(r)
