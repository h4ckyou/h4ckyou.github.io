def finalString(s):
    s = list(s)
    rev = []

    for i in range(len(s)):
        rev.append(s[i])
        if s[i] == 'i':
            rev = rev[::-1]
            rev.pop(rev.index(s[i]))
    

    r = "".join(rev)

    return r
    

s = "string"
r = finalString(s)

print(r)
