def isValid(s):
    parenthesis = {')': '(', '}': '{', ']': '['}
    stack = []

    for char in s:
        if char in parenthesis.values():
            stack.append(char)
        
        elif char in parenthesis.keys():
            if not stack or stack.pop() != parenthesis[char]:
                return False

    return len(stack) == 0

s = "()"
r = isValid(s)

print(r)
