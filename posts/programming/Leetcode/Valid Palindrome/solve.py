import string

def condition(s):
    alphanumeric = list(string.ascii_lowercase + string.digits)
    s = s.split()
    s = "".join(s)
    check = [i for i in s if i in alphanumeric]
    converted = "".join(check)
    
    return converted

def isPalindrome(s):
    charset = condition(s.lower())

    left, right = 0, len(charset)-1

    while left <= right:

        if charset[left] != charset[right]:
            return False
        
        left += 1
        right -= 1

    return True


s = " "
r = isPalindrome(s)

print(r)
