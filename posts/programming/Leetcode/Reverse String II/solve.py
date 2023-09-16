def reverseStr(s, k):
    result = []
    reverse = True 

    for i in range(0, len(s), k):
        chunk = s[i:i + k]
        if reverse:
            result.append(chunk[::-1])
        else:
            result.append(chunk)
        reverse = not reverse

    return "".join(result)


s = "abcdefg"
k = 2
r = reverseStr(s, k)

print(r)
