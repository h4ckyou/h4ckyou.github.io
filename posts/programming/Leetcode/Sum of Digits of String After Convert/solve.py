import string

def getLucky(s, k):
    a = list(string.ascii_lowercase)
    rep = {}
    digit = ""

    for i, j in enumerate(a):
        rep[j] = i + 1
    
    for char in s:
        digit += str(rep[char])

    i = 0

    while True:
        res = digit 
        conv = [int(i) for i in list(str(res))]
        r = 0

        for n in conv:
            r += n

        digit = r

        if i == k-1:
            return r
        else:
            i += 1


s = "iiii"
k = 1

r = getLucky(s, k)
print(r)
