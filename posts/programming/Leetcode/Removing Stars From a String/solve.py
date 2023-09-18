def removeStars(s):
    s = list(s)
    reformed = []

    for i in range(len(s)):
        reformed.append(s[i])
        if reformed[-1] == '*':
            reformed.pop(len(reformed)-1)
            reformed.pop(len(reformed)-1)

    r = "".join(reformed)

    return r

s = "leet**cod*e"
r = removeStars(s)

print(r)
