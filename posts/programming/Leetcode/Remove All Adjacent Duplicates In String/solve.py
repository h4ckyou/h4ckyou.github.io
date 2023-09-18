def removeDuplicates(s):
    stack = [0]

    for i in s:
        if i == stack[-1]:
            stack.pop()
        else:
            stack.append(i)
    
    return "".join(stack[1:])


    
s = "azxxzy"
r = removeDuplicates(s)

print(r)
