def lengthOfLastWord(s):
    r = len(s.split()[-1])

    return r

s = "   fly me   to   the moon  "
r = lengthOfLastWord(s)

print(r)
