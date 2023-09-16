def reverseOnlyLetters(s):
    s = list(s)

    left, right = 0, len(s)-1

    while left < right:

        while left < right and s[left].isalpha() == False:
            left += 1

        while left < right and s[right].isalpha() == False:
            right -= 1
        
        if s[left].isalpha() and s[right].isalpha():
            s[left], s[right] = s[right], s[left]

        
        left += 1
        right -= 1
    
    r = "".join(s)

    return r 


s = "Test1ng-Leet=code-Q!"
r = reverseOnlyLetters(s)

print(r)
