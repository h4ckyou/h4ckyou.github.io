def longestCommonPrefix(strs):
    array = sorted(strs)

    first = array[0]
    last = array[len(strs)-1]
    r = ""

    for i in range(len(first)):
        if first[i] != last[i]:
            break
        else:
            r += first[i]

    if len(r) != 0:
        return r
    else:
        return ""

strs = ["flower","flow","flight"]
r = longestCommonPrefix(strs)

print(r)
