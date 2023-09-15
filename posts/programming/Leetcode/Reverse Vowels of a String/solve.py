def reverseVowels(s):
    s = list(s)
    vowels = {"a", "e", "i", "o", "u", "A", "E", "I", "O", "U"}

    left, right = 0, len(s)-1

    while left < right:

        while left < right and s[left] not in vowels:
            left += 1

        while left < right and s[right] not in vowels:
            right -= 1
        
        if s[left] in vowels and s[right] in vowels:
            s[left], s[right] = s[right], s[left]


        left += 1
        right -= 1


    r = "".join(s)
    
    return r


s = "leetcode"
r = reverseVowels(s)

print(r)
