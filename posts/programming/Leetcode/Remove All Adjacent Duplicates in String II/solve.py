def removeDuplicates(s, k):
    stack = []
    r = []

    for c in s:
        if not stack or stack[-1][0] != c:
            stack.append([c, 1])
        else:
            stack[-1][1] += 1
            
            if stack[-1][1] == k:
                stack.pop()
        
    for char, cnt in stack:
        r.append(char * cnt)
        
    return "".join(r)


s = "yfttttfbbbbnnnnffbgffffgbbbbgssssgthyyyy" 
k = 4
r = removeDuplicates(s, k)

print(r)
